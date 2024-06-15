import os
import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv

SUBJECT = ""
SENDER = ""
RECIPIENT = ""
PASSWORD = ""  # Use Google's App passwords
SHOULD_IMPORT_FROM_ENV = True  # Set this to False if you prefer to enter the data manually above


def import_from_env():
    global SUBJECT, SENDER, RECIPIENT, PASSWORD

    load_dotenv()
    SUBJECT = os.getenv("SUBJECT")
    SENDER = os.getenv("SENDER")
    RECIPIENT = os.getenv("RECIPIENT")
    PASSWORD = os.getenv("PASSWORD")


def generate_alert_mail(new_data, old_data, screenshot):
    new_data_html = ""
    for key in new_data:
        new_data_html += f"<p>{key} : {new_data[key]}</p>"

    old_data_html = ""
    for key in old_data:
        old_data_html += f"<p>{key} : {old_data[key]}</p>"

    body = f"""
    <html>
  <body>
    <h1>URGENT</h1> 
    <h3>A change has been detected</h3>
    <p>The <b>NEW</b> data is <br> <b>{new_data_html}</b></p>
    <br>
    <br>
    <p>The <b>OLD</b> data was <br> <b>{old_data_html}</b></p>
    <br>
    <br>
    <h3>Screenshot is attached below</h3>
  </body>
</html>
    """

    if screenshot:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(screenshot)
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= screenshot.png",
        )
        return body, part

    return body, None


def send_mail(body, attachment):
    if SHOULD_IMPORT_FROM_ENV:
        import_from_env()

    msg = MIMEMultipart()
    msg['Subject'] = SUBJECT
    msg['From'] = SENDER
    msg['To'] = RECIPIENT
    msg.attach(MIMEText(body, "html"))

    if attachment is not None:
        msg.attach(attachment)

    context = ssl.create_default_context()

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.ehlo()
        server.starttls(context=context)
        server.login(SENDER, PASSWORD)
        server.sendmail(SENDER, RECIPIENT, msg.as_string())


def do_alert_mail(new_data, old_data, screenshot):
    body, attachment = generate_alert_mail(new_data, old_data, screenshot)
    send_mail(body, attachment)
