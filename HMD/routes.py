from flask import render_template, url_for, flash, redirect, request
from flask import *
from HMD import app, db, bcrypt
from HMD.forms import RegistrationForm, LoginForm,PatientForm,Up,Search
from HMD.models import User, Post,Patient
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime


@app.route("/")
@app.route("/home")
@login_required
def home():
    return render_template('index.html')


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
        return redirect(url_for('newPatient'))
    return render_template('home.html', title='home',form=form)

@app.route("/update", methods=['GET', 'POST'])
@login_required
def update_info():
    form = Up()
    if request.method == 'POST':
        id_update = request.form.get('id')
        session['id_update'] = id_update
        print(id_update)
        return redirect(url_for('act_update_info',update_id = id_update))
    return render_template('update.html')  

@app.route("/act_update", methods=['GET', 'POST'])
@login_required
def act_update_info():
    form = PatientForm()
    id_update = session.get('id_update',None)
    pat = Patient.query.get(int(id_update))
    field = ["1","3","5","7","9"]
    if form.validate_on_submit():
        if 'Update' in request.form.values():
            pat.ws_pat_name = form.ws_pat_name.data
            pat.ws_age = form.ws_age.data
            pat.ws_doj = form.ws_doj.data
            pat.ws_rtype_name = form.ws_rtype.data
            pat.ws_adrs = form.ws_adrs.data
            db.session.commit()
            flash("Your data has been updated",'success')
            return redirect(url_for('act_update_info'))
        if 'Delete' in request.form.values():
            db.session.delete(pat)
            db.session.commit()
            flash("Your data has been deleted",'success')
            return redirect(url_for('update_info'))
    form.ws_pat_name.data = pat.ws_pat_name
    form.ws_age.data = pat.ws_age
    date_time_obj = datetime.strptime(pat.ws_doj,'%Y-%m-%d')
    form.ws_doj.data = date_time_obj
    form.ws_rtype.data = pat.ws_rtype
    form.ws_adrs.data = pat.ws_adrs

    return render_template('act_update_info.html',form=form,field=field)

@app.route("/view", methods=['GET', 'POST'])
@login_required
def view():
    pat = Patient.query.all()
    return render_template('view.html',pats=pat)


@app.route("/search", methods=['GET', 'POST'])
@login_required
def search():
    form = Search()
    if request.method == 'POST':
        id_update = form.id.data
        pat = Patient.query.get(int(id_update))
        if pat:
            session['id_update'] = id_update
            print(id_update)
            return redirect(url_for('act_update_info',update_id = id_update))
        else:
            flash("Patient doesn't exist")
    
    return render_template('search.html',form=form)
