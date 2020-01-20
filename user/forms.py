import re
from flask_wtf import Form
from wtforms import PasswordField, StringField, validators
from wtforms.fields.html5 import EmailField
from wtforms.widgets import TextArea
from wtforms.validators import ValidationError

from user.models import User


class BaseUserForm(Form):
  first_name = StringField('First Name', [validators.Required()])
  last_name = StringField('Last Name', [validators.Required()])
  email = EmailField('Email Address', [
    validators.DataRequired(),
    validators.Email()
  ])
  username = StringField('Username', [
    validators.Required(),
    validators.length(min=4, max=25)
  ])
  bio = StringField('Bio', widget=TextArea(), validators=[validators.Length(max=60)])

class RegisterForm(BaseUserForm):
  password = PasswordField('New Password', [
    validators.Required(),
    validators.EqualTo('confirm', message='Passwords must match'),
    validators.length(min=4, max=80)
  ])
  confirm = PasswordField('Repeat Password')

  def validate_username(form, field):
    if User.objects.filter(username=field.data).first():
      raise ValidationError('Username already exists')
    if not re.match("^[a-zA-z0-9_-]{4,25}$", field.data):
      raise ValidationError("Invalid username")

  def validate_email(form, field):
    if User.objects.filter(email=field.data).first():
      raise ValidationError("Email is already in use")

class LoginForm(Form):
  username = StringField('Username', [
    validators.DataRequired(),
    validators.length(min=4, max=25)
  ])

  password = PasswordField('Password', [
    validators.DataRequired(),
    validators.length(min=4, max=80)
  ])

class EditForm(BaseUserForm):
  pass