# -*- coding: utf-8 -*-
"""googlemap.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1iYbpj9mtGWe2lZuua074cBLVvqUzirSi

1. Google Maps Integration for Real-Time Tracking
First, you need to integrate the Google Maps API. You can do this in Colab using the gmplot library or by directly embedding Google Maps through JavaScript with the Python Flask library for web development. However, for simplicity, a basic setup for tracking GPS coordinates can be shown:
"""

# Install necessary libraries
!pip install gmplot

# Import libraries
from gmplot import gmplot

# Assuming you have GPS data for elephant location and tourist camps
latitude_list = [6.85, 6.88, 6.87]  # Elephant GPS data
longitude_list = [79.85, 79.89, 79.87]

# Initialize Google Maps Plotter
gmap = gmplot.GoogleMapPlotter(6.85, 79.85, 13)

# Plot elephant movements
gmap.scatter(latitude_list, longitude_list, color='red', size=40, marker=False)

# Draw the map to an HTML file
gmap.draw("elephant_tracking_map.html")

!pip install folium

import folium
from folium import plugins

def create_map(latitude, longitude, zoom_start=12):
    """
    Create an interactive map with a custom marker at specified coordinates.

    Parameters:
    latitude (float): Latitude of the location
    longitude (float): Longitude of the location
    zoom_start (int): Initial zoom level of the map (default: 12)

    Returns:
    folium.Map: Interactive map object
    """
    # Create a map centered at the specified location
    m = folium.Map(location=[latitude, longitude],
                   zoom_start=zoom_start,
                   tiles='OpenStreetMap')

    # Add a marker with a popup
    folium.Marker(
        [latitude, longitude],
        popup='Selected Location',
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)

    # Add a circle around the marker
    folium.Circle(
        radius=1000,  # 1000 meters radius
        location=[latitude, longitude],
        color='crimson',
        fill=True,
    ).add_to(m)

    # Add fullscreen button
    plugins.Fullscreen().add_to(m)

    # Add location finder
    plugins.LocateControl().add_to(m)

    return m

#Upper Diyaluma Waterfall coordinates
latitude = 6.7330
longitude = 81.0330

# Create and display the map
my_map = create_map(latitude, longitude)
my_map

icon=folium.Icon(color='green', icon='info-sign')  # Changes marker to blue

radius=2000  # Changes radius to 2000 meters

tiles='Stamen Terrain'  # Changes to terrain view

"""Elephant Movement Detection with Sensors
The movement detection would rely on AI models trained using sensor data. Here’s a simple framework using Python to process data from thermal, radar, and GPS sensors:
"""

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Simulated dataset of sensor readings (thermal, radar, GPS)
data = np.array([
    [35.2, 1, 78.5],  # Example: temperature, radar distance, GPS proximity
    [34.8, 0, 100.0],
    [36.1, 1, 60.3],
    # Add more data points here
])

labels = np.array([1, 0, 1])  # 1 for elephant detected, 0 for no detection

# Split into training and test sets
X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2)

# Train a simple RandomForestClassifier
clf = RandomForestClassifier()
clf.fit(X_train, y_train)

# Predict the movement of elephants
predictions = clf.predict(X_test)
print(f"Predicted movements: {predictions}")

"""Geofencing for Alerts
The geofencing system can be implemented using simple logic to check if the GPS coordinates of the elephants are within a designated area (tourist camps). Here’s an example:
"""

# Define geofencing boundaries for the tourist camp
tourist_camp_lat =6.7330
tourist_camp_lon = 81.0330
radius = 0.05  # Example radius in degrees

# Function to check if elephant is within the geofence
def is_within_geofence(elephant_lat, elephant_lon, camp_lat, camp_lon, radius):
    distance = np.sqrt((elephant_lat - camp_lat)**2 + (elephant_lon - camp_lon)**2)
    return distance <= radius

# Example elephant GPS data
elephan
    print("Elephant is outside the geofence.")t_lat = 6.87
elephant_lon = 79.87

# Check if elephant is within the camp boundary
if is_within_geofence(elephant_lat, elephant_lon, tourist_camp_lat, tourist_camp_lon, radius):
    print("Elephant is within the geofenced area. Send alert!")
else:

"""Push Notifications for Alerts
For sending notifications to users in real-time, you can use services like Firebase Cloud Messaging (FCM) to send push notifications to mobile devices. Here’s a simplified example of the logic behind triggering notifications when elephants enter a critical zone:
"""

import requests

# Function to send push notification
def send_push_notification(message):
    url = 'https://fcm.googleapis.com/fcm/send'
    headers = {
        'Authorization': 'key=YOUR_SERVER_KEY',
        'Content-Type': 'application/json'
    }
    payload = {
        'to': '/topics/all',  # Targeting all users subscribed to this topic
        'notification': {
            'title': 'Elephant Intrusion Alert!',
            'body': message
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    print(response.text)

# Trigger a notification
send_push_notification("An elephant has been detected near the tourist camp. Evacuate immediately!")

""". Field Deployment of Sensors
You’ll be using Arduino IDE for programming the microcontrollers (e.g., Arduino with ESP8266). Here's a snippet of Python code to simulate data collection and transmission from an IoT sensor network to the cloud for real-time monitoring:
"""

import random
import time

# Simulate IoT sensor data
def simulate_sensor_data():
    temperature = random.uniform(30, 40)  # Simulate temperature data
    radar_distance = random.uniform(50, 150)  # Simulate radar distance
    gps_proximity = random.uniform(70, 120)  # Simulate GPS proximity
    return temperature, radar_distance, gps_proximity

# Simulate real-time sensor data collection
while True:
    temp, radar, gps = simulate_sensor_data()
    print(f"Temperature: {temp}, Radar Distance: {radar}, GPS Proximity: {gps}")

    # Send data to cloud (e.g., AWS, Firebase) here
    time.sleep(2)  # Delay to simulate real-time data collection

"""Machine Learning for Elephant Movement Prediction
You can also build AI models to predict elephant movement using TensorFlow or other ML libraries:
"""

import tensorflow as tf
from tensorflow import keras
import numpy as np  # Import numpy for array creation

# Define a simple neural network for movement prediction
model = keras.Sequential([
    keras.layers.Dense(32, activation='relu', input_shape=(3,)),  # 3 input features
    keras.layers.Dense(16, activation='relu'),
    keras.layers.Dense(1, activation='sigmoid')  # Output: 0 or 1
])

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Create sample training data and labels (replace with your actual data)
# Assuming 100 samples with 3 features each
X_train = np.random.rand(100, 3)
y_train = np.random.randint(0, 2, size=(100, 1))  # Binary labels (0 or 1)

# Create sample test data (replace with your actual test data)
X_test = np.random.rand(20, 3)

# Train the model on sensor data
model.fit(X_train, y_train, epochs=10)

# Make predictions
predictions = model.predict(X_test)
print(f"Predicted movements: {predictions}")

pip install -U googlemaps

pip install nox