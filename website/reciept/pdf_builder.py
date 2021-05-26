from flask import render_template
import pdfkit

def render_email(type_student, name, username):
    pdf_template = render_template('verification.html', type_student = type_student, name = name, username = username)
    pdf = pdfkit.from_string(pdf_template, False)
    email_template = render_template('verification_page.html', name = name, username = username)
    return pdf, email_template