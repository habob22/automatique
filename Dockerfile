FROM ubuntu:20.04

# Set environment variables to non-interactive (this prevents some prompts)
ENV DEBIAN_FRONTEND=noninteractive

# Install Python and pip
RUN apt-get update && \
    apt-get install -y python3.8 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Update symbolic links to python and pip
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.8 1 && \
    update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1

# Set the working directory in the container
WORKDIR /app

# Copy the Python dependencies file to the container
COPY requirements.txt requirements.txt

# Install Python packages from requirements.txt
RUN pip install -r requirements.txt

# Install SSH Client
RUN apt-get update && \
    apt-get install -y openssh-client && \
    rm -rf /var/lib/apt/lists/*

# Copy the source code, models, and data into the container
COPY src/ src/
COPY models/ models/
COPY data/ data/

# Command to run the application
CMD ["python", "src/monitor_traffic.py"]
