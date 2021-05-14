from flask import render_template, url_for, flash, redirect
from website import app, db
from website.forms import VerificationForm, RemovalForm, EmojiForm, TicketForm
from website.models import Verify, Removal, Emoji, Ticket

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html', title = 'About')

@app.route('/events')
def events():
    return render_template('events.html', title = 'Events')

@app.route('/resources')
def resources():
    return render_template('resources.html', title = 'Resources')

@app.route('/gettingstarted')
def gettingstarted():
    return render_template('gettingstarted.html', title = 'Getting Started')

@app.route('/botguide')
def botguide():
    return render_template('botguide.html', title = 'Bot Guide')

@app.route('/forms')
def forms():
    return render_template('forms.html', title = 'Forms')

# Forms
@app.route('/forms/verification', methods=['GET', 'POST'])
def verificationform():
    form = VerificationForm()
    if form.validate_on_submit():
        verify = Verify(type_student = form.user_option.data, email = form.email.data, full_name = form.full_name.data, username = form.discord_username.data)
        db.session.add(verify)
        db.session.commit()
        flash('Thank you for your Verification', 'success')
        return redirect(url_for('forms'))
    return render_template('forms/verificationform.html', title = 'Verification', form = form)

@app.route('/forms/removal', methods=['GET', 'POST'])
def removalform():
    form = RemovalForm()
    if form.validate_on_submit():
        flash('Thank you for your Removal Form', 'success')
        return redirect(url_for('forms'))
    return render_template('forms/removalform.html', title = 'Removal', form = form)

@app.route('/forms/emoji', methods=['GET', 'POST'])
def emojiform():
    form = EmojiForm()
    if form.validate_on_submit():
        flash('Thank you for submitting an Emoji', 'success')
        return redirect(url_for('forms'))
    return render_template('forms/emojiform.html', title = 'Emoji', form = form)

@app.route('/forms/ticket', methods=['GET', 'POST'])
def ticketform():
    form = TicketForm()
    if form.validate_on_submit():
        flash('Thank you for submitting a Ticket', 'success')
        return redirect(url_for('forms'))
    return render_template('forms/ticketform.html', title = 'Ticket', form = form)