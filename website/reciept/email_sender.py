from website import mail
from website.reciept.pdf_builder import build_email
from flask_mail import Message
import smtplib, requests
from email.message import EmailMessage
import os

EMAIL_ADDRESS = os.environ.get('EMAIL_ADD')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')

def verify_email(email):
    response = requests.get('https://isitarealemail.com/api/email/validate', params = {'email': email})
    status = response.json()['status']
    if status == 'invalid':
        return False
    else:
        return True

def EmailReciept(form_type, **kwargs):
    pdf, email_template = build_email(form_type, kwargs)
    filename = f'UCSB Physics Discord {form_type}.pdf'
    try:
        if kwargs["option"]:
            if kwargs["option"] == 'Gaucho':
                email_message = Message('Welcome Gaucho!')
            else:
                email_message = Message('Welcome Future Gaucho!')
    except:
        email_message = Message(f'UCSB Physics Discord {form_type} Response')
    email_message.add_recipient(kwargs["email"])
    email_message.html = email_template
    email_message.attach(filename = filename, content_type = 'application/pdf', data = pdf)
    mail.send(email_message)
