from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
	username = StringField('Username *', validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email *', validators=[DataRequired(), Email()])
	user_type = SelectField('User Type *', choices=[('business_owner','Business Owner'), ('customer','Customer')], validators=[DataRequired()])
	password = PasswordField('Password *', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password *', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Log In')