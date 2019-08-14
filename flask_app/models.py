from datetime import datetime, timedelta
from flask_app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    user_type = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    user_image_file = db.Column(
        db.String(120), nullable=False, default='default.jpg')
    businesses = db.relationship(
        'Business', backref='business_owner', lazy=True)
    reviews = db.relationship('Review', backref='owner', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.user_type}')"


class Business(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    business_title = db.Column(db.String(100), nullable=False)
    business_description = db.Column(db.String(280), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    business_image_file = db.Column(
        db.String(120), nullable=False, default='default.jpg')
    business_date_posted = db.Column(db.DateTime, nullable=False,
                                     default=datetime.utcnow() + timedelta(hours=3))
    business_category = db.Column(db.String(100), nullable=False)
    business_location = db.Column(db.String(100), nullable=False)
    business_tel = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Business('{self.business_title}', '{self.business_date_posted}')"


class Review(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    review_date_posted = db.Column(db.DateTime, nullable=False,
                                   default=datetime.utcnow() + timedelta(hours=3))
    review_content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Review('{self.review_content}', '{self.review_date_posted}'"
