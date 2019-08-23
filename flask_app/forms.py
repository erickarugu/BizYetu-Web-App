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
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError(
                    'That email is taken! Enter another one.')


counties = [("Baringo County", "Baringo County"), ("Bomet County", "Bomet County"), ("Bungoma County", "Bungoma County"), ("Busia County", "Busia County"), ("Elgeyo Marakwet County","Elgeyo Marakwet County"), ("Embu County","Embu County"), ("Garissa County","Garissa County"), ("Homa Bay County","Homa Bay County"), ("Isiolo County","Isiolo County"), ("Kajiado County", "Kajiado County"), ("Kakamega County","Kakamega County"), ("Kericho County","Kericho County"), ("Kiambu County","Kiambu County"), ("Kilifi County","Kilifi County"), ("Kirinyaga County","Kirinyaga County"), ("Kisii County","Kisii County"), ("Kisumu County","Kisumu County"), ("Kitui County","Kitui County"), ("Kwale County","Kwale County"), ("Laikipia County","Laikipia County"), ("Lamu County","Lamu County"), ("Machakos County","Machakos County"), ("Makueni County","Makueni County"), ("Mandera County","Mandera County"), ("Meru County","Meru County"), ("Migori County","Migori County"), ("Marsabit County","Marsabit County"), ("Mombasa County","Mombasa County"), ("Muranga County","Muranga County"), ("Nairobi County","Nairobi County"), ("Nakuru County","Nakuru County"), ("Nandi County","Nandi County"), ("Narok County","Narok County"), ("Nyamira County","Nyamira County"), ("Nyandarua County","Nyandarua County"), ("Nyeri County","Nyeri County"), ("Samburu County","Samburu County"), ("Siaya County","Siaya County"), ("Taita Taveta County","Taita Taveta County"), ("Tana River County","Tana River County"), ("Tharaka Nithi County","Tharaka Nithi County"), ("Trans Nzoia County","Trans Nzoia County"), ("Turkana County","Turkana County"), ("Uasin Gishu County","Uasin Gishu County"), ("Vihiga County","Vihiga County"), ("Wajir County","Wajir County"), ("West Pokot County","West Pokot County")]

business_categories = [('TECHNOLOGY', 'TECHNOLOGY'),('SME', 'SME'), ('AGRICULTURE', 'AGRICULTURE'), ('MANUFACTURING','MANUFACTURING'),('ONLINE','ONLINE')]


class BusinessForm(FlaskForm):
    business_title = StringField(
        'Title', validators=[DataRequired(), Length(min=5, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    business_description = TextAreaField(
        'Description', validators=[DataRequired(), Length(min=10, max=120)])
    business_location = SelectField(
        'Location', choices=counties, validators=[DataRequired()])
    business_category = SelectField(
        'Business Category *', choices=business_categories, validators=[DataRequired()])
    business_tel = StringField('Telephone', validators=[DataRequired()])
    submit = SubmitField('Post')
