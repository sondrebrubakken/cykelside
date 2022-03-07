from turtle import title
from forumside.forms import NyEventForm
from flask import render_template, url_for, flash,redirect, request
from forumside import app, db, bcrypt
from forumside.forms import RegistrationForm, LoginForm, MedlemForm,SubmitForm, RuteForm, NyEventForm
from forumside.models import NyEvent, User, Post, Rute
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
        ruter = Rute(route=form.route.data, name=form.name.data)
        db.session.add(ruter)
        db.session.commit()
        return redirect(url_for('nyruter'))
    return render_template('nyruter.html', title="Nye ruter", form=form, routes=routes)

@app.route('/medlem')
def medlem():
    form = MedlemForm()
    return render_template('medlem.html', title="Bliv Medlem", form=form)

@app.route('/nyevent', methods=['POST','GET'])
def nyevent():
    form = NyEventForm()
    if form.validate_on_submit():
        post = NyEvent(title=form.title.data, content=form.content.data, event_date=form.date.data, rute=form.rute.data, bruger=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('testhome'))
    return render_template('nyevent.html', title='Ny Event', form=form)

@app.route('/testhome')
def testhome():
    posts = NyEvent.query.order_by(NyEvent.event_date.desc())
    return render_template('testhome.html', posts=posts)

@app.route("/event/<int:event_id>")
def event(event_id):
    post = NyEvent.query.get_or_404(event_id)
    return render_template('event.html', post=post)


