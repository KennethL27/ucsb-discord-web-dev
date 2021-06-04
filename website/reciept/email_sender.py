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

# def EmailReciept(type_student, email, name, username):
#     pdf, email_template = build_email(type_student, email, name, username)
#     filename = f'UCSB Physics Discord Verification: {name}.pdf'
#     email_message = EmailMessage()
#     if type_student == 'Gaucho':
#         email_message['Subject'] = 'Welcome Gaucho!'
#     else:
#         email_message['Subject'] = 'Welcome Future Gaucho!'
#     email_message['From'] = EMAIL_ADDRESS
#     email_message['To'] = email
#     email_message.add_alternative(email_template, subtype = 'html')
#     email_message.add_attachment(pdf, maintype = 'application', subtype = 'octet-stream', filename = filename)

#     with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
#         smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
#         smtp.send_message(email_message)

def EmailReciept(type_student, email, name, username):
    pdf, email_template = build_email(type_student, email, name, username)
    filename = f'UCSB Physics Discord Verification: {name}.pdf'
    if type_student == 'Gaucho':
        email_message = Message('Welcome Gaucho!')
    else:
        email_message = Message('Welcome Future Gaucho!')
    email_message.add_recipient(email)
    email_message.html = email_template
    email_message.attach(filename = filename, content_type = 'application/pdf', data = pdf)
    mail.send(email_message)
