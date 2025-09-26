import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time

# ===== MQTT Setup =====
broker = "172.20.10.6"  # IP ?????
topic = "test/data"

client = mqtt.Client()
client.connect(broker, 1883, 60)

# ===== HC-SR04 Setup =====
TRIG = 21
ECHO = 20

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def get_distance():
    # Send 10us pulse to trigger
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    # Wait for echo start
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    # Wait for echo end
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance_cm = pulse_duration * 17150  # speed of sound
    return round(distance_cm, 2)

try:
    while True:
        distance = get_distance()
        payload = {
            "sensor": "ultrasonic",
            "status": f"{distance} cm",
            "time": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        print("Publishing:", payload)
        client.publish(topic, str(payload))
        time.sleep(2)

except KeyboardInterrupt:
    print("Exiting...")

finally:
    GPIO.cleanup()
