import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(sender_email_id, password, receiver_email_id, names, subject, body, attachment_filename):
    message = MIMEMultipart()
    message["From"] = sender_email_id
    message["To"] = receiver_email_id
    message["Subject"] = subject
    message["Bcc"] = receiver_email_id

    message.attach(MIMEText(body, "plain"))

    with open(attachment_filename, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename= {attachment_filename}")
        message.attach(part)
        text = message.as_string()
        context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email_id, password)
        server.sendmail(sender_email_id, receiver_email_id, text)

    print(f'Mail has been send from {sender_email_id} to {receiver_email_id}!!')
