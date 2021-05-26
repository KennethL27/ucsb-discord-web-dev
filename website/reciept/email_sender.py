from website.reciept.pdf_builder import render_email
import smtplib, requests
from email.message import EmailMessage

EMAIL_ADDRESS = 'D'
EMAIL_PASSWORD = 'SD'

def email_check(email):
    response = requests.get('https://isitarealemail.com/api/email/validate', params = {'email': email})
    status = response.json()['status']
    if status == 'invalid':
        return False
    else:
        return True

def EmailReciept(type_student, email, name, username):
    if email_check(email) == False:
        return True
    pdf, email_template = render_email(type_student, name, username)
    filename = f'UCSB Physics Discord Verification: {name}'
    email_message = EmailMessage()
    if type_student == 'Gaucho':
        email_message['Subject'] = 'Welcome Gaucho!'
    else:
        email_message['Subject'] = 'Welcome Future Gaucho!'
    email_message['From'] = EMAIL_ADDRESS
    email_message['To'] = email
    email_message.add_alternative(email_template, subtype = 'html')
    email_message.add_attachment(pdf, maintype = 'application', subtype = 'octet-stream', filename = filename)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(email_message)