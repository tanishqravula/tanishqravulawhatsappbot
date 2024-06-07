import json
from dotenv import load_dotenv
import os
import requests
import aiohttp
import asyncio

# --------------------------------------------------------------
# Load environment variables
# --------------------------------------------------------------

load_dotenv()
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
RECIPIENT_WAID = os.getenv("RECIPIENT_WAID")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
VERSION = os.getenv("VERSION")

APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")

# --------------------------------------------------------------
# Helper functions
# --------------------------------------------------------------

def get_text_message_input(recipient, text):
    return json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient,
            "type": "text",
            "text": {"preview_url": False, "body": text},
        }
    )

def send_message(data):
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}",
    }

    url = f"https://graph.facebook.com/{VERSION}/{PHONE_NUMBER_ID}/messages"

    response = requests.post(url, data=data, headers=headers)
    if response.status_code == 200:
        print("Status:", response.status_code)
        print("Content-type:", response.headers["content-type"])
        print("Body:", response.text)
        return response
    else:
        print(response.status_code)
        print(response.text)
        return response

async def send_message_async(data):
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}",
    }

    async with aiohttp.ClientSession() as session:
        url = f"https://graph.facebook.com/{VERSION}/{PHONE_NUMBER_ID}/messages"
        try:
            async with session.post(url, data=data, headers=headers) as response:
                if response.status == 200:
                    print("Status:", response.status)
                    print("Content-type:", response.headers["content-type"])
                    html = await response.text()
                    print("Body:", html)
                else:
                    print(response.status)
                    print(await response.text())
        except aiohttp.ClientConnectorError as e:
            print("Connection Error", str(e))

# --------------------------------------------------------------
# Send a custom text WhatsApp message to multiple recipients
# --------------------------------------------------------------

def send_messages_to_recipients(recipients, message):
    for recipient in recipients:
        data = get_text_message_input(recipient.strip(), message)
        response = send_message(data)
        print(f"Message sent to {recipient.strip()} with status {response.status_code}")

recipients = RECIPIENT_WAID.split(",")
message = "Hello, this is a test message."

send_messages_to_recipients(recipients, message)

# --------------------------------------------------------------
# Send a custom text WhatsApp message asynchronously to multiple recipients
# --------------------------------------------------------------

async def send_messages_to_recipients_async(recipients, message):
    tasks = []
    for recipient in recipients:
        data = get_text_message_input(recipient.strip(), message)
        tasks.append(send_message_async(data))
    await asyncio.gather(*tasks)

loop = asyncio.get_event_loop()
loop.run_until_complete(send_messages_to_recipients_async(recipients, message))
loop.close()
