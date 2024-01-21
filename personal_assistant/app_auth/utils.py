import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load secret .env file
load_dotenv()


def send_email_via_smtp(receiver_email, subject, body) -> bool:
    """
    The send_email_via_smtp function sends an email to the specified receiver_email address.
    The subject and body of the email are also specified as parameters.

    :param receiver_email: Specify the email address of the recipient
    :param subject: Set the subject of the email
    :param body: Specify the content of the email
    :return: True if the email is sent successfully, and false otherwise
    """
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = int(os.getenv('SMTP_PORT'))
    username = os.getenv('EMAIL_FROM')
    password = os.getenv('SMTP_PASSWORD')

    message = MIMEMultipart()
    message["From"] = username
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(username, password)
            server.sendmail(username, receiver_email, message.as_string())
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
