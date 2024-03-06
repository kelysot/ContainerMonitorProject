# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the app.py file into the container at /app
COPY monitor.py /app/

# Install any needed dependencies specified in requirements.txt
RUN apt-get update -y
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Set the time zone to Israel
ENV TZ=Israel

# Update the system's time zone
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Command to run your Python program
CMD ["python", "monitor.py"]
