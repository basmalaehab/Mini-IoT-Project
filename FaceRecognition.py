import face_recognition
import cv2
import numpy as np
from datetime import datetime
import paho.mqtt.client as paho
import json

# ---------------- MQTT CALLBACKS ----------------
def on_connect(client, userdata, flags, rc):
    print("CONNACK received with " + str(rc))
    # Subscribe to the "Person" topic once connected
    client.subscribe("Person")
    print("Subscribed to topic: Person")

def on_publish(client, userdata, mid):
    print("Message ID: " + str(mid))

def on_message(client, userdata, msg):
    print(f"Received message from topic '{msg.topic}': {msg.payload.decode()}")

# ---------------- MQTT SETUP ----------------
client = paho.Client()
client.username_pw_set("BasmalaEhab", "B@s2442004")
client.tls_set()  # Enable TLS
client.on_connect = on_connect
client.on_publish = on_publish
client.on_message = on_message
client.connect("12e3c1c15bdd48368787154aef22a377.s1.eu.hivemq.cloud", 8883)
client.loop_start()

# ---------------- FACE RECOGNITION SETUP ----------------
video_capture = cv2.VideoCapture(0)

known_face_encodings = [
    face_recognition.face_encodings(face_recognition.load_image_file(f))[0] 
    for f in ["basmala.jpeg", "mahmoud.jpeg"]
]
known_face_names = ["BaSMaLa", "Mahmoud"]

printed_names = set()  # To avoid duplicate publishing

while True:
    ret, frame = video_capture.read()
    if not ret:
        continue

    # Resize frame for faster detection
    small_frame = cv2.resize(frame, (0,0), fx=0.25, fy=0.25)[:, :, ::-1]

    face_locations = face_recognition.face_locations(small_frame)
    scaled_face_locations = [(top*4, right*4, bottom*4, left*4) for (top,right,bottom,left) in face_locations]
    face_encodings = face_recognition.face_encodings(frame, scaled_face_locations)

    face_names = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match = np.argmin(face_distances)
        if matches[best_match]:
            name = known_face_names[best_match]
        face_names.append(name)

        # Publish to MQTT only once per person
        if name != "Unknown" and name not in printed_names:
            printed_names.add(name)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            attendance = {"name": name, "timestamp": timestamp}
            attendance_json = json.dumps(attendance)
            client.publish("attendance", attendance_json, qos=1)
            print(f"Published: {attendance_json}")

    # Draw rectangles and labels
    for (top, right, bottom, left), name in zip(scaled_face_locations, face_names):
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1) 

    # Show video
    cv2.imshow("Video", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
video_capture.release()
cv2.destroyAllWindows()
client.loop_stop()
client.disconnect()
