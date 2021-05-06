from flask import Flask, render_template, url_for, flash, redirect
from forms import VerificationForm, RemovalForm, EmojiForm, TicketForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '174d7cc25e44491b940fe0c792640e9f'

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
        flash('Thank you for your Verification', 'success')
        return redirect(url_for('forms'))
    return render_template('verificationform.html', title = 'Verification', form = form)

@app.route('/forms/removal', methods=['GET', 'POST'])
def removalform():
    form = RemovalForm()
    if form.validate_on_submit():
        flash('Thank you for your Removal Form', 'success')
        return redirect(url_for('forms'))
    return render_template('removalform.html', title = 'Removal', form = form)

@app.route('/forms/emoji', methods=['GET', 'POST'])
def emojiform():
    form = EmojiForm()
    if form.validate_on_submit():
        flash('Thank you for submitting an Emoji', 'success')
        return redirect(url_for('forms'))
    return render_template('emojiform.html', title = 'Emoji', form = form)

@app.route('/forms/ticket', methods=['GET', 'POST'])
def ticketform():
    form = TicketForm()
    if form.validate_on_submit():
        flash('Thank you for submitting a Ticket', 'success')
        return redirect(url_for('forms'))
    return render_template('ticketform.html', title = 'Ticket', form = form)

if __name__ == '__main__':
    app.run(debug = True)