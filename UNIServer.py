import paho.mqtt.client as paho
import json
import csv
from datetime import datetime
import os

CSV_FILE = "attendance_records.csv"

# Ensure CSV file exists and write header if it doesn't
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Timestamp", "Received At"])  # Add "Received At" for local timestamp

# Called when the client subscribes to a topic
def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: " + str(mid) + " QoS: " + str(granted_qos))

# Called when a message is received
def on_message(client, userdata, msg):
    try:
        message = msg.payload.decode()
        data = json.loads(message)  # Parse JSON
        print(f"Topic: {msg.topic} | Name: {data['name']} | Timestamp: {data['timestamp']}")

        # Append to CSV immediately
        with open(CSV_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([data['name'], data['timestamp'], datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
    except json.JSONDecodeError:
        print(f"Received non-JSON message: {msg.payload.decode()}")

client = paho.Client()
client.username_pw_set("BasmalaEhab", "B@s2442004")
client.tls_set()  # Enable TLS

client.on_subscribe = on_subscribe
client.on_message = on_message

client.connect("12e3c1c15bdd48368787154aef22a377.s1.eu.hivemq.cloud", 8883)

# Subscribe to the "attendance" topic
client.subscribe("attendance", qos=1)

# Start listening for messages indefinitely
client.loop_forever()
