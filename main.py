import datetime

import simplejson as simplejson
from flask import Flask, render_template, url_for, flash, redirect, request
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from flask_login import login_user, current_user, logout_user, login_required, LoginManager, UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    password = db.Column(db.String(60), nullable=False)
    tickets = db.relationship('Ticket', backref='owner', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(100), nullable=False)
    category = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Ticket('{self.event}', '{self.category}', '{self.price}', '{self.date}', '{self.user_id}')"


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


tickets = [
    {
        'event': 'Enter Shikari',
        'date': '31.11.2018',
        'category': 'music',
        'price': '1000'
    },
    {
        'event': 'Stoned Jesus',
        'date': '21.11.2018',
        'category': 'music',
        'price': '400'
    },
    {
        'event': 'Avengers 14',
        'date': '11.11.2018',
        'category': 'film',
        'price': '200'
    },
    {
        'event': 'Carpet',
        'date': '01.11.2018',
        'category': 'film',
        'price': '10'
    },
    {
        'event': 'MC Mcdonalds',
        'date': '05.01.2019',
        'category': 'misc',
        'price': '5000'
    },
    {
        'event': 'New Year with real Santa',
        'date': '31.12.2018',
        'category': 'misc',
        'price': '1000000'
    },
]


@app.route("/")
@app.route("/store")
@login_required
def home():
    return render_template('home.html', tickets=tickets)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
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
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():

    tickets_as_json = []

    try:
        all_tickets = Ticket.query.all()

        for ticket in all_tickets:
            ticket_as_json = {
                'event': ticket.event,
                'price': ticket.price,
                'date': ticket.date}
            tickets_as_json.append(ticket_as_json)

    except ValueError:
        flash('Can\'t load tickets', 'danger')

    json = simplejson.dumps(ticket_as_json)

    image_file = url_for('static', filename='pics/' + 'default.png')
    return render_template('account.html', title='Account',
                           image_file=image_file, tickets=json)


if __name__ == '__main__':
    app.run(debug=True)
