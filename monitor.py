""" Group 2 code - trying to modify in order to connect the 2 parts we worked on"""
import fcntl
import random
from concurrent.futures import ProcessPoolExecutor

import docker
import psutil
import os
import time
import sqlite3
from datetime import datetime

LOCK_FILE = '/app/instance/db_lock.lock'
first_write_to_db = True


def acquire_lock():
    try:
        lockfile = open(LOCK_FILE, 'w')
        fcntl.flock(lockfile, fcntl.LOCK_EX)
    except Exception as e:
        print(f"Error occurred while acquiring lock: {e}")


def release_lock():
    try:
        lockfile = open(LOCK_FILE, 'w')
        fcntl.flock(lockfile, fcntl.LOCK_UN)
    except Exception as e:
        print(f"Error occurred while releasing lock: {e}")


def get_container_status(container_id):
    global first_write_to_db

    # Connect to Docker daemon
    client = docker.from_env()

    # Get container object
    container = client.containers.get(container_id)

    # Fetch container stats
    container_stats = container.stats(stream=False)

    # Extract CPU stats
    cpu_stats = container_stats['cpu_stats']
    cpu_usage = cpu_stats['cpu_usage']['total_usage']
    cpu_system = cpu_stats['system_cpu_usage']

    # Calculate CPU percentage
    cpu_percent = round((cpu_usage / cpu_system) * 100, 2)

    # Get container memory stats
    used_memory = container_stats['memory_stats']['usage']
    memory_gb = used_memory / (1024 ** 3)  # Memory usage in GB
    max_memory = container_stats['memory_stats']['limit']
    percent_used_memory = round((float(used_memory) / max_memory) * 100, 2)

    # Get host disk stats
    disk_stats = psutil.disk_usage('/')
    disk_used_gb = disk_stats.used / (1024 ** 3)
    disk_free_gb = disk_stats.free / (1024 ** 3)  # Disk space in GB
    disk_percent = round((disk_stats.used / disk_stats.total) * 100, 2)

    # Get number of processes
    num_processes = len(psutil.pids())

    container_data = {}
    if first_write_to_db:
        container_data["Container Id"] = container_id
        container_data["Memory Total"] = f"{max_memory / (1024 ** 3):.2f}"
        container_data["Disk Total"] = f"{disk_stats.total / (1024 ** 3):.2f}"

    metrices_data = {
        "Time Stamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "CPU Percent": cpu_percent,
        "Memory Used": f"{memory_gb:.2f}",
        "Memory Percent": percent_used_memory,
        "Disk Percent": disk_percent,
        "Disk Used": f"{disk_used_gb:.2f}",
        "Number of Processes": num_processes
    }

    processes_info = []
    for proc in psutil.process_iter():
        with proc.oneshot():
            try:
                process_info = {
                    'pid': proc.pid,
                    'name': proc.name(),
                    'cpu_percent': f"{proc.cpu_percent():.2f}",
                    'memory_percent': f"{proc.memory_percent():.2f}",
                    'cmdline': ' '.join(proc.cmdline()),
                    'username': proc.username(),
                    'num_threads': proc.num_threads(),
                    'status': proc.status(),
                    'create_time': proc.create_time(),
                    'num_fds': proc.num_fds(),
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                processes_info.append(process_info)
            except psutil.Error as e:
                print(f"Error occurred while accessing process info: {e}")

    return container_data, metrices_data, processes_info


def write_container_data_to_db(c, conn, container_data):
    container_query = (
        "INSERT INTO Container (container_id, memory_total, disk_total) "
        "SELECT ?, ?, ? "
        "WHERE NOT EXISTS (SELECT 1 FROM Container WHERE container_id = ?)"
    )
    container_values = [
        container_data[key] for key in ["Container Id", "Memory Total", "Disk Total"]
    ]
    # Append the container_id again for the WHERE clause in the query
    container_values.append(container_data["Container Id"])
    c.execute(container_query, container_values)
    conn.commit()


def write_processes_data_to_db(c, conn, processes_data):
    try:
        for process in processes_data:
            c.execute("INSERT INTO Processes (pid, name, cpu_percent, memory_percent, "
                      "cmdline, username, num_threads, status, create_time, num_fds, timestamp) "
                      "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                      (process['pid'], process['name'], process['cpu_percent'],
                       process['memory_percent'], process['cmdline'], process['username'],
                       process['num_threads'], process['status'], process['create_time'],
                       process['num_fds'], process['timestamp']))
        conn.commit()  # Commit the transaction after all processes have been inserted
    except Exception as e:
        print(f"Error occurred while writing processes data to the database: {e}")
        conn.rollback()


def write_metrics_data_to_db(c, conn, metrics_data):
    metrics_query = ("INSERT INTO Metrics (timestamp, cpu_percent, memory_used, memory_percent, disk_percent, "
                     "disk_used, num_processes) "
                     "VALUES (?, ?, ?, ?, ?, ?, ?)")
    metrics_values = [metrics_data[key] for key in
                      ["Time Stamp", "CPU Percent", "Memory Used", "Memory Percent", "Disk Percent", "Disk Used",
                       "Number of Processes"]]
    c.execute(metrics_query, metrics_values)
    conn.commit()


def write_to_db():
    global first_write_to_db
    while True:
        acquire_lock()
        try:
            # Connect to SQLite database
            conn = sqlite3.connect('/app/instance/site.db')
            c = conn.cursor()

            container_id = os.environ.get('HOSTNAME')  # Get the container ID
            container_data, metrics_data, processes_data = get_container_status(container_id)

            if first_write_to_db:
                write_container_data_to_db(c, conn, container_data)
                first_write_to_db = False

            write_metrics_data_to_db(c, conn, metrics_data)
            write_processes_data_to_db(c, conn, processes_data)

            conn.close()
            release_lock()
            time.sleep(6)

        except KeyboardInterrupt:
            print("Program terminated by user.")
        finally:
            conn.close()
            release_lock()


def random_sleep_time():
    return random.uniform(2, 10)


def memory_bound_task():
    # This function performs a Memory-bound task
    for i in range(20):
        a = []
        for i in range(10 ** 7):
            a.append(i)
            a.append(i)
        time.sleep(random_sleep_time() * 2)


def cpu_bound_task():
    # This function performs a CPU-bound task
    for i in range(20):
        result = 0
        for i in range(10 ** 7):  # Reduced iterations
            result += i
        time.sleep(random_sleep_time())


def disk_bound_task():
    # This function performs a disk-bound task
    for i in range(20):
        file_name = 'file.txt'
        file_size_mb = 100  # File size in MB
        file_size_bytes = file_size_mb * (1024 ** 2)  # Convert MB to bytes
        write_chunk_size = 4096  # Chunk size for writing to the file

        for i in range(10 ** 7):  # Reduced iterations
            # Generate a large file to simulate disk-bound task
            with open(file_name, 'wb') as f:
                for _ in range(file_size_bytes // write_chunk_size):
                    f.write(os.urandom(write_chunk_size))

            # Reading the file to simulate disk-bound task
            with open(file_name, 'rb') as f:
                data = f.read()

            # Cleanup: Delete the file after task completion
            time.sleep(random_sleep_time())
        os.remove(file_name)


if __name__ == '__main__':
    with ProcessPoolExecutor() as executor:
        executor.submit(write_to_db)
        for task in [memory_bound_task, cpu_bound_task, disk_bound_task]:
            executor.submit(task)
