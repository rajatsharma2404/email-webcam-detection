import os
import smtplib
from email.message import EmailMessage
import imghdr

SENDER = "avataraang384@gmail.com"
PASSWORD = os.getenv("PASSWORD4")
RECEIVER = "avataraang384@gmail.com"

def send_email(image_path):
    print("send_email function started")
    email_message = EmailMessage()
    email_message["Subject"] = "A new customer just showed up"
    email_message.set_content("Hey, we just had a new customer")

    with open(image_path, "rb") as file:
        attachment = file.read()

    email_message.add_attachment(attachment, maintype = "image", subtype = imghdr.what(None, attachment))

    #creating a mail server with host "smtp.gmail.com" and port 587
    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER, PASSWORD)
    gmail.sendmail(SENDER, RECEIVER, email_message.as_string())
    gmail.quit()
    print("send_email function ended")

if __name__ == "__main__":
    send_email("images/20.png")

