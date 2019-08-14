import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from flask_app import app, db, bcrypt
from flask_app.models import User, Business
from flask_app.forms import RegistrationForm, LoginForm, UpdateAccountForm, BusinessForm
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html', title='Home')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data,
                    user_type=form.user_type.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'{form.username.data}, Your account has been created', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'Login Unsuccessful. Please check your Email and Password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about_us.html', title='About')


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)

    return picture_fn


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    businesses = Business.query.filter_by(
        user_id=current_user.id).order_by(Business.business_date_posted.desc()).first()
    total_businesses = Business.query.filter_by(
        user_id=current_user.id).order_by(Business.business_date_posted.desc()).count()
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.user_image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.user_type = form.user_type.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.user_type.data = current_user.user_type
    image_file = url_for(
        'static', filename='profile_pics/' + current_user.user_image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form, businesses=businesses, total_businesses=total_businesses)


@app.route('/businesses', methods=['GET', 'POST'])
def businesses():
    businesses = Business.query.order_by(
        Business.business_date_posted.desc()).all()
    return render_template('businesses.html', title='Businesses', businesses=businesses)


@app.route('/businesses/new', methods=['GET', 'POST'])
@login_required
def new_business():
    form = BusinessForm()

    if form.validate_on_submit():
        business = Business(business_title=form.business_title.data, email=form.email.data, business_description=form.business_description.data,
                            business_location=form.business_location.data, business_category=form.business_category.data, business_tel=form.business_tel.data, business_owner=current_user)
        db.session.add(business)
        db.session.commit()
        flash('Your Business has been posted', 'success')
        return redirect(url_for('home'))
    return render_template('create_business.html', title="New Business", form=form)


# @app.route("/post/<int:business_id>")
# def business(business_id):
#     business = Business.query.get_or_404(business_id)
#     return render_template('business.html', title='business.business_title')
