# Use an Ubuntu base image with Python 3.8 installed
FROM ubuntu:20.04

# Avoiding user interaction with tzdata
ENV DEBIAN_FRONTEND=noninteractive

# Set the working directory in the container
WORKDIR /app

# Install Python and pip
RUN apt-get update && apt-get install -y python3.8 python3-pip

# Copy the Python dependencies file to the container
COPY requirements.txt requirements.txt

# Install Python packages from requirements.txt
RUN python3.8 -m pip install -r requirements.txt

# Install OpenSSH client
RUN apt-get install -y openssh-client

# Clean up to keep the image tidy
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the source code, models, and data into the container
COPY src/ src/
COPY models/ models/
COPY data/ data/

# Command to run the application
CMD ["python3.8", "src/monitor_traffic.py"]
