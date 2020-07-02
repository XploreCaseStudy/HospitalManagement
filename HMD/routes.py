from flask import render_template, url_for, flash, redirect, request
from flask import *
from HMD import app, db, bcrypt
from HMD.forms import Up,Search
from datetime import datetime
from HMD.forms import Done,Clear,NewMForm,MedicineForm,RegistrationForm, LoginForm,PatientForm,DiagnosisForm,NewDForm
from HMD.models import temp,User,Patient,Diagnostics,PatientDiagnostics,Medicines,PatientMedicine
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
@login_required
def home():
    return render_template('index.html')


@app.route("/about")
@login_required
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
        flash("Patient Data Created",'success')
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
            return redirect(url_for('sresult',update_id = id_update))
        else:
            flash("Patient doesn't exist",'success')
    
    return render_template('search.html',form=form)

@app.route("/sresult", methods=['GET', 'POST'])
@login_required
def sresult():
    form = PatientForm()
    temp.query.delete()
    PatientDiagnostics.query.delete()
    PatientMedicine.query.delete()
    id_update = session.get('id_update',None)
    tempId = temp(id=id_update)
    db.session.add(tempId)
    db.session.commit()
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
            return redirect(url_for('sresult'))
        if 'Delete' in request.form.values():
            db.session.delete(pat)
            db.session.commit()
            flash("Your data has been deleted",'success')
            return redirect(url_for('sresult'))
        if 'Issue Medicines' in request.form.values():
            return redirect(url_for('medicine',update_id = id_update,pat = pat))
        if 'Add Diagnostics' in request.form.values():
            return redirect(url_for('diagnosis',update_id = id_update,pat = pat))
    form.ws_pat_name.data = pat.ws_pat_name
    form.ws_age.data = pat.ws_age
    date_time_obj = datetime.strptime(pat.ws_doj,'%Y-%m-%d')
    form.ws_doj.data = date_time_obj
    form.ws_rtype.data = pat.ws_rtype
    form.ws_adrs.data = pat.ws_adrs
    return render_template('sresult.html',form=form,field=field)


@app.route("/Diagnostics", methods=['GET', 'POST'])
@login_required
def diagnosis():
    ds = Diagnostics.query.all()
    # p = Patient.query.first()
    id = request.args.get('update_id', None)
    print("id:", id)
    tempID = temp.query.first()
    print("ID:", tempID)
    p = Patient.query.filter_by(id=tempID.id).first()
    print("YUHOOO!!:",p)
    form = DiagnosisForm()
    form2 = NewDForm()
    clear = Clear()
    # if clear.validate_on_submit():
    #     PatientDiagnostics.query.delete().where(PatientDiagnostics.ws_pat_name == p.ws_pat_name)
    #     return redirect(url_for('Diagnostics'))
    if form2.validate_on_submit():
        check = Diagnostics.query.filter_by(test_name=form2.dName.data).first()
        print("CHECK:", check)
        if check is None:
            x = Diagnostics(test_name = form2.dName.data,
                        charge = form2.charge.data)
            db.session.add(x)
            db.session.commit()
            flash("New Diagnosis Added!", 'success')
            return redirect(url_for('diagnosis'))
        else:
            flash("Diagnosis Already present!", 'success')
    d = None
    if form.validate_on_submit():
        d = form.dname.data
        checkIfExists = PatientDiagnostics.query.filter_by(test_id=d.id).first()
        if checkIfExists is None:
            dp = PatientDiagnostics(patient_id = p.id,test_id = d.id,
                                    ws_pat_name = p.ws_pat_name,
                                    test_name = d.test_name,
                                    charge = d.charge)
            db.session.add(dp)
            db.session.commit()
        else:
            flash("Diagnosis Already Entered!", 'success')
    x = PatientDiagnostics.query.all()#ps = p
    return render_template('diagnostics.html', title='diagnosis',ps = p,clear=clear,x=x,ds = ds,form = form,form2 = form2,d =d)

@app.route("/medicine", methods=['GET', 'POST'])
@login_required
def medicine():
    ds = Medicines.query.all()
    # p = Patient.query.first()
    id = request.args.get('update_id', None)
    print("id:",id)
    tempID = temp.query.first()
    print("ID:", tempID)
    p = Patient.query.filter_by(id=tempID.id).first()
    form = MedicineForm()
    form2 = NewMForm()
    clear = Clear()
    # if clear.validate_on_submit():
    #     q = PatientMedicine.query.get(p.id)
    #     db.session.delete(q)
    #     return redirect(url_for('medicine'))
    if form2.validate_on_submit():
        check = Medicines.query.filter_by(m_name=form2.mName.data).first()
        print("CHECK:",check)
        if check is None:
            x = Medicines(m_name = form2.mName.data,
                            charge = form2.charge.data,
                          quantity =  form2.quantity.data)
            db.session.add(x)
            db.session.commit()
            flash("New Medicines Added!", 'success')
            return redirect(url_for('medicine'))
        else:
            flash("Medicines Already Exists!", 'success')
    d = None
    if form.validate_on_submit():
        d = form.mname.data
        checkIfExists = PatientMedicine.query.filter_by(m_id=d.id).first()
        if checkIfExists is None:
            dp = PatientMedicine(patient_id = p.id,m_id = d.id,
                                    ws_pat_name = p.ws_pat_name,
                                    m_name = d.m_name,
                                    charge = d.charge,
                                 quantity = form.quantity.data)
            check = Medicines.query.filter_by(m_name=d.m_name).first()
            if d.quantity >= form.quantity.data:
                db.session.query(Medicines).filter(Medicines.m_name == d.m_name).\
                    update({Medicines.quantity: Medicines.quantity - form.quantity.data}, synchronize_session=False)
                db.session.add(dp)
                db.session.commit()
            else:
                flash("Currently Not Available", 'success')
        else:
            flash("Medicines Already Entered!", 'success')
    x = PatientMedicine.query.filter(PatientMedicine.ws_pat_name == p.ws_pat_name)#ps = p
    return render_template('medicines.html',ps=p, title='medicines',clear=clear,x=x,ds = ds,form = form,form2 = form2,d =d)


@app.route("/bill", methods=['GET', 'POST'])
@login_required
def bill():
    ps = Patient.query.first()
    m = PatientMedicine.query.all()
    d = PatientDiagnostics.query.all()
    p = 0
    for dia in d:
        print(dia.charge)
        p = p+ dia.charge
    for med in m:
        print(med.charge * med.quantity)
        p = p + (med.charge * med.quantity)
    form = Done()
    if form.validate_on_submit():
        temp.query.delete()
        PatientDiagnostics.query.delete()
        PatientMedicine.query.delete()
        return redirect(url_for('home'))
    return render_template('bill.html', form=form,title='bill',p = p,m = m,x=d,ps = ps)