from flask import render_template
import pdfkit

def build_email(form_type, values):
    pdf_template = render_template(f'reciept/{form_type}_pdf.html', values = values)
    pdf = pdfkit.from_string(pdf_template, False)
    email_template = render_template(f'reciept/{form_type}_email.html', values = values)
    return pdf, email_template