import paho.mqtt.client as mqtt

# ---------------- MQTT SETUP ----------------
def on_connect(client, userdata, flags, rc):
    print("CONNACK received with " + str(rc))  

def on_publish(client, userdata, mid):
    print("Message ID: " + str(mid))

client = mqtt.Client()
client.username_pw_set("BasmalaEhab","B@s2442004")
client.tls_set()  
client.on_connect = on_connect
client.on_publish = on_publish

client.connect("12e3c1c15bdd48368787154aef22a377.s1.eu.hivemq.cloud", 8883)
client.loop_start()

# ---------------- WAIT FOR USER ----------------
print("Press 'c' then Enter to publish to MQTT topic 'PersonDetected'")
key = input().strip().lower()

if key == 'c':
    # Publish simple message to PersonDetected topic
    message = "PersonDetected"
    client.publish("PersonDetected", message, qos=1)
    print(f"Published to PersonDetected: {message}")
