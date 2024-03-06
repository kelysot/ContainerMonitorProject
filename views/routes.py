import threading
import time
from datetime import datetime, timedelta

from flask import render_template, jsonify

from Models.Metrics import Metrics
from Models.Container import Container
from Models.Processes import Processes
from database import app, db
import fcntl

data_dict = dict()
container_dict = dict()
cur_processes = dict()
data_dict_all = dict()


def save_container_data_locally():
    global container_dict

    acquire_lock()
    with app.app_context():
        # Retrieve the last container record
        last_container_record = Container.query.order_by(Container.id.desc()).first()

        # Extract necessary information from the container records
        if last_container_record:
            container_dict = {
                'Container ID': last_container_record.container_id,
                'Total Memory':last_container_record.memory_total,
                'Total Disk': last_container_record.disk_total
            }

    release_lock()


def initialize_app():
    # Start the thread for saving data periodically
    thread = threading.Thread(target=save_data_locally, args=(app,))
    thread.daemon = True  # Set the thread as a daemon, so it exits when the main thread exits
    thread.start()

    save_container_data_locally()

    @app.route("/")
    def homepage():
        is_empty = db.session.query(Metrics).count() == 0
        if not is_empty:
            return render_template("homepage.html")
        else:
            return render_template("no_data.html")

    @app.route("/no_data")
    def no_data():
        return render_template("no_data.html")


def generate_plot(metric_type, data_dict_to_use, data_type):
    if data_type != "last_day":
        labels = [datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").strftime("%H:%M:%S") for timestamp in
                  data_dict_to_use.get('Timestamp')]
    else:
        labels = data_dict_to_use.get('Timestamp')

    return {
        "data": data_dict_to_use.get(metric_type),
        "labels": labels,
        "metric_type": metric_type
    }


def generate_plots_by_type(data_type):
    global data_dict_all

    timestamps = data_dict_all.get('Timestamp', [])
    filtered_data = {}
    current_time = datetime.now()

    if data_type == "last_hour":
        # Calculate the starting time for the last hour
        last_hour = current_time - timedelta(hours=1)

        # Filter timestamps within the last hour
        timestamps_list = [timestamp for timestamp in timestamps if
                           datetime.fromisoformat(timestamp) >= last_hour]
    elif data_type == "last_day":
        # Calculate the starting time for the last day
        last_day = current_time - timedelta(hours=24)

        # Filter timestamps within the last day
        timestamps_list = [timestamp for timestamp in timestamps if
                           datetime.fromisoformat(timestamp) >= last_day]
    else:
        timestamps_list = timestamps

    # Calculate the number of timestamps to select with equal gaps
    num_timestamps_to_select = 10

    for key, value_list in data_dict_all.items():
        # Extract values corresponding to filtered timestamps (assuming timestamps are at index 0)
        filtered_values = [value for timestamp, value in zip(timestamps_list, value_list) if
                           timestamp in timestamps_list]

        # Add filtered values to the result dictionary with the same key
        filtered_data[key] = filtered_values

    # Calculate the step size for selecting timestamps
    if num_timestamps_to_select < len(timestamps_list):
        step_size = len(timestamps_list) // num_timestamps_to_select
    else:
        step_size = 1

    # Select timestamps with equal gaps
    selected_timestamps = timestamps_list[::step_size]
    # Create a new dictionary with only selected timestamps
    result_data = {key: [] for key in filtered_data.keys()}  # Create empty dictionary
    for timestamp in selected_timestamps:
        for key, value_list in filtered_data.items():
            # Find the index of the matching timestamp
            index = value_list.index(filtered_data[key][0]) if timestamp == timestamps_list[
                0] else value_list.index(filtered_data[key][timestamps_list.index(timestamp)])
            result_data[key].append(value_list[index])

    plots = {}
    for metric_type in ['CPU', 'Memory', 'Disk', 'Processes', 'Memory Used', 'Disk Used']:
        plots[metric_type] = generate_plot(metric_type, result_data, data_type)

    return tuple(plots.values())


LOCK_FILE = 'instance/db_lock.lock'


def acquire_lock():
    lockfile = open(LOCK_FILE, 'w')
    fcntl.flock(lockfile, fcntl.LOCK_EX)


def release_lock():
    lockfile = open(LOCK_FILE, 'w')
    fcntl.flock(lockfile, fcntl.LOCK_UN)


def save_metrics_data():
    global data_dict, data_dict_all
    try:
        metrics_cols = {'Timestamp': Metrics.timestamp,
                        'CPU': Metrics.cpu_percent,
                        'Memory Used': Metrics.memory_used,
                        'Memory': Metrics.memory_percent,
                        'Disk': Metrics.disk_percent,
                        'Disk Used': Metrics.disk_used,
                        'Processes': Metrics.num_processes}
        for key, column in metrics_cols.items():
            # Modify the query to retrieve only the last 10 records
            query_result = Metrics.query.with_entities(column) \
                .order_by(Metrics.timestamp.desc()) \
                .limit(10).all()

            query_result_all = Metrics.query.with_entities(column) \
                .order_by(Metrics.timestamp.desc()) \
                .all()

            if key == 'Timestamp':
                data_dict[key] = [str(date[0]) for date in query_result]
                data_dict_all[key] = [str(date[0]) for date in query_result_all]
            elif key == 'Processes':
                data_dict[key] = [int(process[0]) for process in query_result]
            else:
                data_dict[key] = [float(result[0]) for result in query_result]
                data_dict_all[key] = [float(result[0]) for result in query_result_all]
    except Exception as e:
        print(f"Error occurred in save_metrics_data: {e}")


def save_processes_data():
    global cur_processes
    try:
        processes_cols = {'PID': Processes.pid,
                          'Name': Processes.name,
                          'CPU': Processes.cpu_percent,
                          'Memory': Processes.memory_percent,
                          'Cmdline': Processes.cmdline,
                          'Username': Processes.username,
                          'Num Threads': Processes.num_threads,
                          'Num FDs': Processes.num_fds,
                          'Status': Processes.status,
                          'Timestamp': Processes.timestamp
                          }
        for key, column in processes_cols.items():
            # Modify the query to retrieve only the last 10 records
            query_result = Processes.query.with_entities(column) \
                .order_by(Processes.timestamp.desc()) \
                .limit(10).all()

            # Process query results based on the attribute key
            if key in ['PID', 'Num FDs', 'Num Threads']:
                cur_processes[key] = [int(item[0]) for item in query_result]
            elif key in ['Name', 'Status', 'Cmdline', 'Username', 'Timestamp']:
                cur_processes[key] = [str(item[0]) for item in query_result]
            else:
                cur_processes[key] = [float(item[0]) for item in query_result]
    except Exception as e:
        print(f"Error occurred in save_processes_data: {e}")
    return cur_processes


def save_data_locally(app):
    with app.app_context():
        while True:
            acquire_lock()
            try:
                save_metrics_data()
                save_processes_data()
            finally:
                release_lock()
            time.sleep(30)


@app.route('/processes')
def processes():
    global cur_processes
    return render_template("processes.html", processes=cur_processes)


# Route to fetch metrics plot data
@app.route('/get_metrics')
def get_metrics():
    global data_dict
    try:
        is_empty = db.session.query(Metrics).count() == 0
        if not is_empty:
            cpu_plot = generate_plot('CPU', data_dict, "over_time")
            memory_plot = generate_plot('Memory', data_dict, "over_time")
            disk_plot = generate_plot('Disk', data_dict, "over_time")
            processes_plot = generate_plot('Processes', data_dict, "over_time")

            memory_used_plot = generate_plot('Memory Used', data_dict, "over_time")
            disk_used_plot = generate_plot('Disk Used', data_dict, "over_time")

            all_memory = data_dict["Memory"]
            used_mem = data_dict["Memory Used"]
            memory_total = container_dict.get('Total Memory')
            disk_total = container_dict.get('Total Disk')

            # locals() function is used to create a dictionary containing all the local variables in the current scope.
            return jsonify(**locals())
        else:
            return jsonify(message="No data available in the database")

    except Exception as e:
        print(f"Error occurred in get_metrics: {e}")
        return jsonify(message="An error occurred while fetching metrics data.")


@app.route('/get_process_metrics')
def get_process_metrics():
    """Fetch process metrics data."""
    processes_data = save_processes_data()
    return jsonify(processes_data=processes_data)


# Route to fetch metrics plot data
@app.route('/get_hour_metrics')
def get_hour_metrics():
    (last_hour_cpu_plot, last_hour_memory_plot, last_hour_disk_plot, last_hour_processes_plot,
     last_hour_memory_used_plot, last_hour_disk_used_plot) = generate_plots_by_type("last_hour")

    # locals() function is used to create a dictionary containing all the local variables in the current scope.
    return jsonify(**locals())


# Route to fetch metrics plot data
@app.route('/get_day_metrics')
def get_day_metrics():
    (last_day_cpu_plot, last_day_memory_plot, last_day_disk_plot, last_day_processes_plot,
     last_day_memory_used_plot, last_day_disk_used_plot) = generate_plots_by_type("last_day")

    # locals() function is used to create a dictionary containing all the local variables in the current scope.
    return jsonify(**locals())
