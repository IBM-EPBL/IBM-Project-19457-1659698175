from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

import os
from dotenv import load_dotenv

load_dotenv()

def SendEmail(email, username):
    FROM_EMAIL =  "plasmadonarapp@gmail.com"
    TEMPLATE_ID = os.getenv("SENDGRID_TEMPLATE_ID")
    key = os.getenv("SENDGRID_KEY")

    message = Mail(from_email = FROM_EMAIL,
    to_emails= email)

    message.dynamic_template_data = {
        'name': username
    }
    
    message.template_id = TEMPLATE_ID

    try:
        sg = SendGridAPIClient(key)
        response = sg.send(message)
        code, body, headers = response.status_code, response.body, response.headers
        print(f"Response code: {code}")
        print(f"Response headers: {headers}")
        print(f"Response body: {body}")
        print("Dynamic Messages Sent!")
    except Exception as e:
        print(e)
