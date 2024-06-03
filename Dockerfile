FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the Python dependencies file to the container
COPY requirements.txt requirements.txt

# Install Python packages from requirements.txt
RUN pip install -r requirements.txt

# Install system packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends openssh-client && \
    rm -rf /var/lib/apt/lists/*

# If openssh-client is not found, recreate sources.list (Uncomment if needed)
# RUN echo "deb http://deb.debian.org/debian buster main" > /etc/apt/sources.list && \
#     echo "deb http://security.debian.org/debian-security buster/updates main" >> /etc/apt/sources.list && \
#     apt-get update && \
#     apt-get install -y openssh-client

# Copy the source code, models, and data into the container
COPY src/ src/
COPY models/ models/
COPY data/ data/

# Command to run the application
CMD ["python", "src/monitor_traffic.py"]
