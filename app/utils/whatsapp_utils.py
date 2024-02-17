import logging
from flask import current_app, jsonify
import json
import requests
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import textwrap
from bs4 import BeautifulSoup
import base64 
import PIL.Image
import google.generativeai as genai
# from app.services.openai_service import generate_response
import re
GOOGLE_API_KEY='AIzaSyAHoNfvJhI4SwWqC75VfLS33mueiK23g2w'
def load_model() -> genai.GenerativeModel:
    """
    The function load_model() returns an instance of the genai.GenerativeModel class initialized with the model name
    'gemini-pro'.
    :return: an instance of the genai.GenerativeModel class.
    """
    model = genai.GenerativeModel('gemini-pro-vision')
    return model
def generate_content(model_type, content):
    model = genai.GenerativeModel(model_type)
    response = model.generate_content(content)
    return response.text

genai.configure(api_key=GOOGLE_API_KEY)

model = load_model()
def generate_pdf_summary(summary_text):
    # Create a PDF file
    pdf_filename = "summary.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)

    # Set the font and size for the PDF content
    c.setFont("Helvetica", 12)
    heading = ""

    # Initialize variables for the first page
    text_lines = textwrap.wrap(summary_text, width=70)

    # Add the heading to the first page
    c.drawString(50, 750, heading)

    y_position = 730
    for line in text_lines:
        # Check the remaining space on the current page
        remaining_space = y_position - 50

        if remaining_space < 15:
            # Start a new page if the remaining space is not enough for a new line
            c.showPage()
            y_position = 780  # Adjust for new page

            # Add the heading to the new page
            c.drawString(50, 750,"")

        c.drawString(50, y_position, line)
        y_position -= 15  # Adjust for line spacing

    # Save the PDF
    c.showPage()
    c.save()

    return pdf_filename
    
def get_binary_file_downloader_html(bin_file, file_label='Download PDF'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    base64_pdf = base64.b64encode(data).decode()
    pdf_download_link = f'<a href="data:application/pdf;base64,{base64_pdf}" download="{file_label}.pdf">{file_label}</a>'
    return pdf_download_link



def log_http_response(response):
    logging.info(f"Status: {response.status_code}")
    logging.info(f"Content-type: {response.headers.get('content-type')}")
    logging.info(f"Body: {response.text}")


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


def generate_response(response):
    response=response.lower()
    # Return text in uppercase
    if "created" in response and "you" in response and "tube" not in response and "com" not in response  and len(response)<=30:
        return "I was created by Tanishq Ravula"
    if "developed" in response and "you" in response and "tube" not in response and "com" not in response  and len(response)<=30:
        return "I was created by Tanishq Ravula"
    if "invented" in response and "you" in response and "tube" not in response and "com" not in response  and len(response)<=30:
        return "I was created by Tanishq Ravula"
    if "created" in response and "u" in response and "tube" not in response and "com" not in response  and len(response)<=30:
        return "I was created by Tanishq Ravula"
    if "developed" in response and "u" in response and "tube" not in response and "com" not in response  and len(response)<=30:
        return "I was created by Tanishq Ravula"
    if "invented" in response and "u" in response and "tube" not in response and "com" not in response  and len(response)<=30:
        return "I was created by Tanishq Ravula"
    if "create" in response and "you" in response and "tube" not in response and "com" not in response  and len(response)<=30:
        return "I was created by Tanishq Ravula"
    if "develop" in response and "you" in response and "tube" not in response and "com" not in response  and len(response)<=30:
        return "I was created by Tanishq Ravula"
    if "invent" in response and "you" in response and "tube" not in response and "com" not in response  and len(response)<=30:
        return "I was created by Tanishq Ravula"
    if "create" in response and "u" in response and "tube" not in response and "com" not in response  and len(response)<=30:
        return "I was created by Tanishq Ravula"
    if "develop" in response and "u" in response and "tube" not in response and "com" not in response  and len(response)<=30:
        return "I was created by Tanishq Ravula"
    if "invent" in response and "u" in response and "tube" not in response and "com" not in response  and len(response)<=30:
        return "I was created by Tanishq Ravula"
    if "trained" in response and "you" in response and "tube" not in response and "com" not in response  and len(response)<=30:
        return "I was created by Tanishq Ravula"
    if "trained" in response and "u" in response and "tube" not in response and "com" not in response  and len(response)<=30:
        return "I was created by Tanishq Ravula"
    if "train" in response and "you" in response and "tube" not in response and "com" not in response  and len(response)<=30:
        return "I was created by Tanishq Ravula"
    if "train" in response and "u" in response and "tube" not in response and "com" not in response  and len(response)<=30:
        return "I was created by Tanishq Ravula"
    
        
    
    return generate_content("gemini-pro",response)

def send_message(data):
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {current_app.config['ACCESS_TOKEN']}",
    }

    url = f"https://graph.facebook.com/{current_app.config['VERSION']}/{current_app.config['PHONE_NUMBER_ID']}/messages"

    try:
        response = requests.post(
            url, data=data, headers=headers, timeout=10
        )  # 10 seconds timeout as an example
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.Timeout:
        logging.error("Timeout occurred while sending message")
        return jsonify({"status": "error", "message": "Request timed out"}), 408
    except (
        requests.RequestException
    ) as e:  # This will catch any general request exception
        logging.error(f"Request failed due to: {e}")
        return jsonify({"status": "error", "message": "Failed to send message"}), 500
    else:
        # Process the response as normal
        log_http_response(response)
        return response


def process_text_for_whatsapp(text):
    # Remove brackets
    pattern = r"\【.*?\】"
    # Substitute the pattern with an empty string
    text = re.sub(pattern, "", text).strip()

    # Pattern to find double asterisks including the word(s) in between
    pattern = r"\*\*(.*?)\*\*"

    # Replacement pattern with single asterisks
    replacement = r"*\1*"

    # Substitute occurrences of the pattern with the replacement
    whatsapp_style_text = re.sub(pattern, replacement, text)

    return whatsapp_style_text


def process_whatsapp_message(body):
    wa_id = body["entry"][0]["changes"][0]["value"]["contacts"][0]["wa_id"]
    name = body["entry"][0]["changes"][0]["value"]["contacts"][0]["profile"]["name"]

    message = body["entry"][0]["changes"][0]["value"]["messages"][0]
    message_body = message["text"]["body"]

    # TODO: implement custom function here
    response = generate_response(message_body)

    # OpenAI Integration
    # response = generate_response(message_body, wa_id, name)
    # response = process_text_for_whatsapp(response)

    data = get_text_message_input(current_app.config["RECIPIENT_WAID"], response)
    send_message(data)


def is_valid_whatsapp_message(body):
    """
    Check if the incoming webhook event has a valid WhatsApp message structure.
    """
    return (
        body.get("object")
        and body.get("entry")
        and body["entry"][0].get("changes")
        and body["entry"][0]["changes"][0].get("value")
        and body["entry"][0]["changes"][0]["value"].get("messages")
        and body["entry"][0]["changes"][0]["value"]["messages"][0]
    )
