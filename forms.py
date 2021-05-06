from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField, SelectMultipleField, TextAreaField, FileField, widgets, ValidationError
from wtforms.validators import DataRequired, Email, Optional

class MultipleCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class VerificationForm(FlaskForm):
    user_option = RadioField('', validators = [DataRequired()], choices = ["Current UCSB Student or UCSB Faculty", "Prospective UCSB Student"])
    email = StringField('Email Address', validators = [DataRequired(), Email()])
    full_name = StringField('Full Name', validators = [DataRequired()])
    discord_username = StringField('Discord Username and #', validators = [DataRequired()])
    submit = SubmitField('Submit')

    email_check = ''
    def validate_discord_username(self, discord_username):
        if '#' not in discord_username.data or not discord_username.data[-4].isdigit():
            raise ValidationError('The Discord Username should follow this format: PhysicsLegends#6877.')
    def validate_user_option(self, user_option):
        global email_check
        email_check = user_option.data
    def validate_email(self, email):
        global email_check
        if email_check == 'Current UCSB Student or UCSB Faculty':
            if ('ucsb.edu' or 'umail.ucsb.edu') not in email.data:
                raise ValidationError('For UCSB Students and Faculty please use a valid ucsb email.')

class RemovalForm(FlaskForm):
    reason = MultipleCheckboxField('', _prefix="reason", choices=[('1', 'Graduating and no longer need the Server'), ('2', 'Switching Majors'), ('3', 'This community is not for me')])
    other = StringField('Other: ', _prefix="reason")
    email = StringField('Email Address', validators = [DataRequired(), Email()])
    discord_username = StringField('Discord Username and #', validators = [DataRequired()])
    comments = TextAreaField('Comments or Concerns:')
    submit = SubmitField('Submit')

    # Need to check if email and username is already in the database

class EmojiForm(FlaskForm):
    discord_username = StringField('Discord Username and #', validators = [DataRequired()])
    description = TextAreaField('Please provide a detail description if you do not have an image to upload:', validators = [Optional()])
    image = FileField('If you already have a image you would like to see become an emoji in the Server please upload it here:', validators = [Optional()])
    submit = SubmitField('Submit')

    # need to check if username is already in the database

    # Requires one of the fields to be filled in 
    def validate(self):
        if not super(EmojiForm, self).validate():
            return False
        if not self.description.data and not self.image.data:
            error_message = 'Please enter a description or image'
            self.image.errors.append(error_message)
            self.description.errors.append(error_message)
            return False
        return True

class TicketForm(FlaskForm):
    ticket_type = RadioField('', validators = [DataRequired()],
                             choices = ["Ticket another user", "Ticket the functionality of a Bot", "Ticket a staff member"])
    discord_username = StringField('Discord Username and #', validators = [DataRequired()])
    discord_username_against = StringField('If applicable please provide the Discord Username and # of the user being ticked against', validators = [DataRequired()])
    description = TextAreaField('Issue:')
    submit = SubmitField('Submit')

    # need to check if both usernames are in the database


