from flask import render_template
import pdfkit

def build_email(type_student, email, name, username):
    pdf_template = render_template('reciept/verification_pdf.html', type_student = type_student, email = email, name = name, username = username)
    pdf = pdfkit.from_string(pdf_template, False)
    email_template = render_template('reciept/verification_email.html', type_student = type_student, email = email, name = name, username = username)
    return pdf, email_template