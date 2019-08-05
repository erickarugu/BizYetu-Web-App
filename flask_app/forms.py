from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_app.models import User


class RegistrationForm(FlaskForm):
    username = StringField(
        'Username *', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email *', validators=[DataRequired(), Email()])
    user_type = SelectField('User Type *', choices=[(
        'Business Owner', 'Business Owner'), ('Customer', 'Customer')], validators=[DataRequired()])
    password = PasswordField('Password *', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password *', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'That username is taken! Choose another one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'That email is taken! Enter another one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class UpdateAccountForm(FlaskForm):
    username = StringField(
        'Username *', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email *', validators=[DataRequired(), Email()])
    user_type = SelectField('User Type *', choices=[(
        'Business Owner', 'Business Owner'), ('Customer', 'Customer')], validators=[DataRequired()])
    picture = FileField('Update Profile Picture', validators=[
                        FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    'That username is taken! Choose another one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    'That email is taken! Enter another one.')


class BusinessForm(FlaskForm):
    business_title = StringField('Title', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    business_description = TextAreaField(
        'Description', validators=[DataRequired])
    business_location = StringField('Location', validators=[DataRequired()])
    business_category = SelectField('Business Category *', choices=[(
        'TECHNOLOGY', 'TECHNOLOGY'), ('SME', 'SME')], validators=[DataRequired()])
    submit = SubmitField('Post')
