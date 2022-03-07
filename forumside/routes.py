from turtle import title
from flask import render_template, url_for, flash,redirect, request
from forumside import app, db, bcrypt
from forumside.forms import RegistrationForm, LoginForm, MedlemForm,SubmitForm, RuteForm
from forumside.models import User, Post, Rute
from flask_login import login_user, current_user, logout_user, login_required

events = [
    {
        'author': 'Sondre',
        'title': 'Event',
        'content': 'Rulleskøjter er gay'
    },
    {
        'author': 'Mats',
        'title': 'Event2',
        'content': 'Din Mor'
    }
]


@app.route('/')
def home():
    return render_template('home.html', events=events)


@app.route('/about')
def about():
    return render_template('about.html', title="About")

@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Account has been created", 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title="Register", form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else: 
            flash('Wrong username or password', 'danger')
    return render_template('login.html', title="Login", form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/account')
@login_required
def account():
    return render_template('account.html', title="Account")

@app.route('/ruter', methods=['POST', 'GET'])
def ruter():
    adr = SubmitForm()
    return render_template('ruter.html', adr=adr)

@app.route('/nyruter', methods=['POST', 'GET'])
def nyruter():
    form = RuteForm()
    routes = Rute.query.order_by(Rute.id)
    if form.validate_on_submit():
        ruter = Rute(route=form.route.data)
        db.session.add(ruter)
        db.session.commit()
        return redirect(url_for('nyruter'))
    return render_template('nyruter.html', title="Nye ruter", form=form, routes=routes)

@app.route('/medlem')
def medlem():
    form = MedlemForm()
    return render_template('medlem.html', title="Bliv Medlem", form=form)

