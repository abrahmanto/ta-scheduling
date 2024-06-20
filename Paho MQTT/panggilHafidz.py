import requests
import schedule
import queue
import paho.mqtt.client as mqtt
import time
import threading

# Queue for holding HTTP requests
request_queue = queue.Queue()

# MQTT Broker configuration
MQTT_BROKER = "192.168.195.203"
MQTT_PORT = 1883
MQTT_TOPIC_REQUEST = "selenium/request"

# Setup MQTT client
mqtt_client = mqtt.Client()

# Function to process MQTT messages
def on_message(client, userdata, message):
    request_data = message.payload.decode("utf-8").split(",")
    process_id = request_data[0]
    url = request_data[1]
    request_queue.put((process_id, url))

# Connect MQTT client
mqtt_client.connect(MQTT_BROKER, MQTT_PORT)
mqtt_client.subscribe(MQTT_TOPIC_REQUEST)
mqtt_client.on_message = on_message
mqtt_client.loop_start()


# Function to process HTTP requests
def process_requests():
    while True:
        try:
            # Get request data from the queue
            request_data = request_queue.get(timeout=1)
            process_id, url = request_data

            # Construct HTTP request
            # api_endpoint = "http://localhost:8000/trigger_selenium"
            api_endpoint = "http://192.168.195.129:8000/trigger_selenium"
            payload = {"process_id": process_id, "url": url}
            response = requests.request(api_endpoint, data=payload)
            

            # Handle response
            if response.status_code == 200:
                print("I'm in. Ngerjain ", process_id)
            else:
                print("I'm not in, tidak ngerjain ", process_id)

        except queue.Empty:
            # If the queue is empty, wait for a while before checking again
            time.sleep(1)
            continue


# import requests

# url = "http://192.168.195.129:8000/trigger_selenium?process_id=Anto&url=http://updmember.pii.or.id/index.php"

# payload = ""
# headers = {}

# response = requests.request("POST", url, headers=headers, data=payload)

# print(response.text)
#dari postman


# Start a separate thread to process HTTP requests from the queue
request_processing_thread = threading.Thread(target=process_requests)
request_processing_thread.start()

# Schedule HTTP requests
def schedule_requests():
    # Add your scheduling logic here
    # For example, let's schedule a request every minute
    process_id = "21060118140129"
    url = "http://updmember.pii.or.id/index.php"
    request_queue.put((process_id, url))

# Schedule the request every minute
# schedule.every(5).seconds.do(schedule_requests)

schedule_requests()

# Main loop to run the scheduling
# while True:
#     schedule.run_pending()
#     time.sleep(1)