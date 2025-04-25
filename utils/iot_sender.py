import os
import json
from dotenv import load_dotenv
from azure.iot.device import IoTHubDeviceClient, Message

# Load .env file
load_dotenv()

# Get IoT Hub connection string
CONNECTION_STRING = os.getenv("IOTHUB_CONNECTION_STRING")

def send_to_iot_hub(data):
    """Send structured receipt data to Azure IoT Hub."""
    if not CONNECTION_STRING:
        print("❌ IOTHUB_CONNECTION_STRING not found in .env")
        return

    try:
        print("🔌 Connecting to Azure IoT Hub...")
        client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
        print("✅ Connected.")

        # Send the receipt data as a JSON message
        message = Message(json.dumps(data))
        print(f"📤 Sending message: {data}")
        client.send_message(message)
        print("✅ Data sent to Azure IoT Hub!")

        client.shutdown()

    except Exception as e:
        print(f"❌ Failed to send to IoT Hub: {e}")