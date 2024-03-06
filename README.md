# Container Monitor Project

The Container Monitor Project is a web-based container monitoring tool built using Flask.

This application provides real-time, hourly, and daily updates on the system's health, including CPU usage, memory utilization, disk space, and active processes. 
The goal is to help users monitor their system's performance through a user-friendly web interface.

This project is developed with Python, Flask, Docker, SQLite, JavaScript, AJAX, HTML, and CSS.

## Features
- Real-time monitoring of CPU usage, memory utilization, disk space, and active processes.
- REST API architecture for handling HTTP requests.
- Database connectivity to SQLite using SQLAlchemy ORM for reading data, and writing data via Python script inside the container using SQL queries.
- Utilizes AJAX to refresh metrics periodically without reloading the page.
- Locks for Data Consistency: The project utilizes locks to ensure data consistency and prevent race conditions during database write operations. By employing locks around critical database write operations, the system guarantees that only one thread can execute these writes at a time, mitigating the risk of potential data corruption. Moreover, careful consideration is given to prevent deadlock situations, ensuring the smooth operation of the application under concurrent access scenarios.
 
## Technologies 

- *Flask*: A Python web framework for building web applications.
- *SQLAlchemy*: An SQL toolkit and Object-Relational Mapping (ORM) library for Python.
- *HTML/CSS*: For structuring and styling the web application's frontend.
- *AJAX*: Asynchronous JavaScript for reading data from a web server and updating the web page without reloading it.
- *Docker*: Used to create and run containers.

## Prerequisites

Before running the project, ensure you have the following prerequisites installed and set up:

- Python 3
- pip
- Docker

## Installation

1. Clone the repository:
   ```bash
      git clone https://github.com/kelysot/ContainerMonitorProject.git

2. Create a python virtual environment
   ```bash
      python3 -m venv ./venv

3. Open the virtual environment
   - On Windows:
     ```bash
     .\venv\Scripts\activate

   - On Unix or MacOS:
     ```bash
      source ./venv/bin/activate
4. Install the required dependencies:
   ```bash
      pip install -r ./requirements.txt
5. Create the Docker image:
    ```bash
    docker build -t new_image:0.0.1 .
6. Create and run the Docker container: (replace YOUR_PATH with the path to the project on your computer)
    ```bash
    docker run -v /var/run/docker.sock:/var/run/docker.sock -v YOUR_PATH:/app/instance --name new_container new_image:0.0.1
7. Run Flask app.

## Images
- Disk Usage - Host, Memory Usage, and CPU Usage Over Time:

![disk_memory_screenshot](/images/disk_memory_screenshot.png)

- Memory Usage in the Last Hour and Memory Usage in the Last Day:

![memory_screenshot](/images/memory_screenshot.png)

- CPU Usage in the Last Hour and CPU Usage in the Last Day:

![cpu_screenshot](/images/cpu_screenshot.png)


## Participants

[Eden Arni](https://github.com/edenarni), [Waleed Ali](https://github.com/waleed399), Michal Burshtein, and [Kely Sotsky](https://github.com/kelysot)
