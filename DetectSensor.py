from gpiozero import DistanceSensor
from time import sleep
import paho.mqtt.client as mqtt

# ---------------- MQTT SETUP ----------------
def on_connect(client, userdata, flags, rc):
    print("CONNACK received with " + str(rc))              

def on_publish(client, userdata, mid):
    print("Message ID: " + str(mid))

client = mqtt.Client()
client.username_pw_set("BasmalaEhab","B@s2442004")
client.tls_set()  # Enable TLS
client.on_connect = on_connect
client.on_publish = on_publish

client.connect("12e3c1c15bdd48368787154aef22a377.s1.eu.hivemq.cloud", 8883)
client.loop_start()

# ---------------- DISTANCE SENSOR SETUP ----------------
sensor = DistanceSensor(echo=24, trigger=23)
THRESHOLD_CM = 20
person_detected = False

print("Monitoring distance...")

while True:
    distance = sensor.distance * 100  
    print(f"Distance: {distance:.1f} cm")

    if distance < THRESHOLD_CM and not person_detected:
        print(f"Distance < {THRESHOLD_CM} cm, publishing to MQTT...")
        message = "PersonDetected"
        client.publish("PersonDetected", message, qos=1)
        print(f"Published: {message}")
        person_detected = True

    if distance >= THRESHOLD_CM and person_detected:
        person_detected = False

    sleep(0.5)
