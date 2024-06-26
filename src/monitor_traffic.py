import time
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import load_model
from sklearn.preprocessing import normalize
import paramiko
import os

# Load the trained binary classification model
model = load_model('models/worst_normalised9959.h5')

# Use an absolute path for the log file
log_file_path = os.path.abspath('output_log.txt')

# Open a log file to write print outputs
log_file = open(log_file_path, 'a')

def custom_print(*args, **kwargs):
    """
    Custom print function that writes to both the console and a log file.
    """
    print(*args, **kwargs)  # Print to console
    print(*args, **kwargs, file=log_file, flush=True)  # Print to log file and flush immediately

def parse_file(sftp, remote_file_path, last_position):
    counts = {'DIS': 0, 'DIO': 0, 'DAO': 0, 'DATA': 0}
    versions = set()
    ranks = set()
    features_list = []

    with sftp.open(remote_file_path, 'r') as file:
        file.seek(last_position)
        new_lines = file.readlines()
        last_position = file.tell()

        for line in new_lines:
            if 'Paquet DIS' in line:
                counts['DIS'] += 1
            if 'Paquet DIO' in line:
                counts['DIO'] += 1
            if 'Paquet DAO' in line:
                counts['DAO'] += 1
            if 'DATA' in line:
                counts['DATA'] += 1
            if 'Version est :' in line:
                version = int(line.split('Version est :')[1].split()[0])
                versions.add(version)
            if 'Rank est :' in line:
                rank = int(line.split('Rank est :')[1].split()[0])
                ranks.add(rank)

    for version in versions:
        for rank in ranks:
            features = np.zeros(6)
            features[0] = version
            features[1] = rank
            features[2] = counts['DIO']
            features[3] = counts['DIS']
            features[4] = counts['DAO']
            features[5] = counts['DATA']
            features_list.append(features)

    return counts, versions, ranks, features_list, last_position

def predict_with_model(model, features):
    """Make a binary prediction using the trained model and normalized features."""
    # Normalize features using L1 normalization
    features = normalize([features], norm='l1')

    # Reshape data to fit into Conv1D
    features_array = np.expand_dims(features, axis=-1)

    prediction = model.predict(features_array)
    binary_prediction = (prediction < 0.5).astype("int32")

    # Interpret the predicted class
    if binary_prediction == 0:
        return "Pas d'attaque "
    else:
        return "Attaque "

# Remote connection details
hostname = '192.168.8.141'
port = 22
username = 'ubuntu'
password = 'ubuntu'
remote_file_path = '/home/ubuntu/Desktop/contiki/tools/cooja/build/statistiques.txt'
last_position = 0

# Establish SSH connection
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname, port, username, password)
sftp = ssh.open_sftp()

try:
    while True:
        counts, versions, ranks, features_list, last_position = parse_file(sftp, remote_file_path, last_position)

        for features in features_list:
            prediction = predict_with_model(model, features)

            # Display the results
            normalized_features = normalize([features], norm='l1')
            custom_print(f"Counts: {counts}")
            custom_print(f"Version: {features[0]}")
            custom_print(f"Rank: {features[1]}")
            custom_print(f"Normalized Features: {normalized_features}")
            custom_print(f"Sum of Normalized Features: {np.sum(normalized_features)}")
            custom_print(f"Prediction: {prediction}")

        # Wait 60 seconds before reading the file again
        time.sleep(60)
finally:
    sftp.close()
    ssh.close()
    log_file.close()  # Ensure to close the log file at the end
