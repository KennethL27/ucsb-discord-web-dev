from flask import render_template, url_for, flash, redirect, request, Response
from website import app, db, bcrypt
from website.forms import VerificationForm, RemovalForm, EmojiForm, TicketForm, AdminSignin
from website.models import Verify, Removal, Emoji, Ticket, Admin
from website.reciept.email_sender import EmailReciept
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('nav_pages/about.html', title = 'About')

@app.route('/events')
def events():
    return render_template('nav_pages/events.html', title = 'Events')

@app.route('/resources')
def resources():
    return render_template('nav_pages/resources.html', title = 'Resources')

@app.route('/gettingstarted')
def gettingstarted():
    return render_template('nav_pages/gettingstarted.html', title = 'Getting Started')

@app.route('/botguide')
def botguide():
    return render_template('nav_pages/botguide.html', title = 'Bot Guide')

@app.route('/forms')
def forms():
    return render_template('nav_pages/forms.html', title = 'Forms')

# Forms
@app.route('/forms/verification', methods=['GET', 'POST'])
def verificationform():
    form = VerificationForm()
    if form.validate_on_submit():
        verify = Verify(type_user = form.user_option.data, email = form.email.data, full_name = form.full_name.data, username = form.discord_username.data, isreciept = form.isreciept.data)
        db.session.add(verify)
        db.session.commit()
        if form.isreciept.data:
            EmailReciept('verification', option = form.user_option.data, email = form.email.data, name = form.full_name.data, username = form.discord_username.data)
        flash('Thank you for your Verification', 'success')
        return redirect(url_for('forms'))
    return render_template('forms/verificationform.html', title = 'Verification', form = form)

@app.route('/forms/removal', methods=['GET', 'POST'])
def removalform():
    form = RemovalForm()
    if form.validate_on_submit():
        removal = Removal(reason = str(form.reason.data), other_reason = form.other.data, email = form.email.data, username = form.discord_username.data, comments = form.comments.data, isreciept = form.isreciept.data)
        db.session.add(removal)
        db.session.query(Verify).filter_by(username = form.discord_username.data).delete()
        db.session.commit()
        if form.isreciept.data:
            checks = {}
            for value in form.reason.data:
                if value == '1':
                    checks[f'check{value}'] = 'Graduating and no longer need the Server'
                elif value == '2':
                    checks[f'check{value}'] = 'Switching Majors'
                elif value == '3':
                    checks[f'check{value}'] = 'This community is not for me'
            if not form.other.data:
                other = ''
            else:
                other = form.other.data
            if not form.comments.data:
                comments = ''
            else:
                comments = form.comments.data
            EmailReciept('removal', checks = checks, other = other, email = form.email.data, username = form.discord_username.data, comments = comments)
        flash('Thank you for your Removal Form', 'success')
        return redirect(url_for('forms'))
    return render_template('forms/removalform.html', title = 'Removal', form = form)

@app.route('/forms/emoji', methods=['GET', 'POST'])
def emojiform():
    form = EmojiForm()
    if form.validate_on_submit():
        file = request.files['image']
        emoji_image = file.read()
        emoji_image_name = secure_filename(file.filename)
        emoji_image_type = file.mimetype
        emoji = Emoji(username = form.discord_username.data, description = form.description.data, emoji_image = emoji_image, emoji_image_name = emoji_image_name, emoji_image_type = emoji_image_type)
        db.session.add(emoji)
        db.session.commit()
        flash('Thank you for submitting an Emoji', 'success')
        return redirect(url_for('forms'))
    return render_template('forms/emojiform.html', title = 'Emoji', form = form)

@app.route('/forms/ticket', methods=['GET', 'POST'])
def ticketform():
    form = TicketForm()
    if form.validate_on_submit():
        ticket = Ticket(type_ticket = form.ticket_type.data, username = form.discord_username.data, against_username = form.discord_username_against.data, issue = form.description.data, isreciept = form.isreciept.data)
        db.session.add(ticket)
        db.session.commit()
        if form.isreciept.data:
            if not form.discord_username_against.data:
                username2 = ''
            else:
                username2 = form.discord_username_against.data
            email = Verify.query.filter_by(username = form.discord_username.data).first().email
            EmailReciept('ticket', ticket_type = form.ticket_type.data, username = form.discord_username.data, username2 = username2, issue = form.description.data, email = email)
        flash('Thank you for submitting a Ticket', 'success')
        return redirect(url_for('forms'))
    return render_template('forms/ticketform.html', title = 'Ticket', form = form)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if current_user.is_authenticated:
        return redirect(url_for('admin_home'))
    form = AdminSignin()
    if form.validate_on_submit():
        user = Admin.query.filter_by(username = form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('admin_home'))
        else:
            flash('Login Unsuccessful, Username or Password was incorrect')
    return render_template('admin/admin_sign_in.html', title = 'ADMIN', form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/admin/home', methods=['GET', 'POST'])
@login_required
def admin_home():
    emoji_list = db.session.query(Emoji.id).all()
    emoji_ids = [entry.id for entry in emoji_list]
    return render_template('admin/admin_home.html', title = 'ADMIN | HOME', verify_data = Verify.query.all(), removal_data = Removal.query.all(), 
                            Emoji_data = Emoji.query.all(), ticket_data = Ticket.query.all(), emoji_ids = emoji_ids)

# removing login_required to allow the api to send viable links to client
@app.route('/admin/image/<int:id>')
def get_emoji_image(id):
    emoji_image = Emoji.query.filter_by(id=id).first()
    return Response(emoji_image.emoji_image, mimetype=emoji_image.emoji_image_type)