from flask import render_template, url_for, flash, redirect, request
from HMD import app, db, bcrypt
from HMD.forms import RegistrationForm, LoginForm,PatientForm
from HMD.models import User, Post,Patient
from flask_login import login_user, current_user, logout_user, login_required


posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route("/")
@app.route("/home")
def home():
    form = PatientForm()
    form = form
    return render_template('home.html',form=form)


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
        user = User(username=form.username.data, password=hashed_password)
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
        user = User.query.filter_by(username=form.username.data).first()
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
    return redirect(url_for('login'))


@app.route("/patient", methods=['GET', 'POST'])
@login_required
def newPatient():
    form = PatientForm()
    if form.validate_on_submit():
        patient = Patient(ws_pat_name = form.ws_pat_name.data,
                          ws_adrs = form.ws_adrs.data,
                          ws_age = form.ws_age.data,
                          ws_doj = form.ws_doj.data,
                          ws_rtype = form.ws_rtype.data)
        db.session.add(patient)
        db.session.commit()
        flash("Patient Data Created")
        return redirect(url_for('home'))
    return render_template('home.html', title='home',form=form)