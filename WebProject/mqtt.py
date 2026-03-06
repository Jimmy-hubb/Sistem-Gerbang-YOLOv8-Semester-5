# mqtt.py
import paho.mqtt.client as mqtt
import ssl
import os

MQTT_BROKER = os.environ.get("MQTT_BROKER", "19fef3da3cb34dcf9fb18a1e46b8ebf1.s1.eu.hivemq.cloud")
MQTT_PORT = int(os.environ.get("MQTT_PORT", 8883))

MQTT_USERNAME = os.environ.get("MQTT_USER", "web-arduino")
MQTT_PASSWORD = os.environ.get("MQTT_PASS", "WebArduino1")

# topics (must match main.py)
TOPIC_KENDALI = "gate/kendali"      # web publishes commands here
TOPIC_STATUS  = "gate/gerbang"      # main.py publishes gate status here

client = mqtt.Client(client_id="webserver-gate-001")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("[MQTT] Connected SUCCESS")
        client.subscribe(TOPIC_STATUS)
    else:
        print("[MQTT] MQTT Failed, code:", rc)

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
    except:
        payload = str(msg.payload)
    print(f"[MQTT] {msg.topic}: {payload}")

client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.tls_set(cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2)
client.on_connect = on_connect
client.on_message = on_message

def run_mqtt():
    print("[MQTT] Connecting...")
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()
    print("[MQTT] Loop started")

def publish_message(msg):
    client.publish(TOPIC_KENDALI, msg)
    print("[MQTT] Publish:", msg)
