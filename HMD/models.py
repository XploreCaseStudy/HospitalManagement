from datetime import datetime
from HMD import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class temp(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.image_file}')"

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ws_pat_name = db.Column(db.String(100), nullable=False)
    ws_adrs = db.Column(db.String(100), nullable=False)
    ws_age = db.Column(db.String(10), nullable=False)
    ws_doj = db.Column(db.String(100), nullable=False)
    ws_rtype = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"{self.id},{self.ws_pat_name}, {self.ws_adrs}, {self.ws_age},{self.ws_doj},{self.ws_rtype}"


class Diagnostics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_name = db.Column(db.String(100), nullable=False)
    charge = db.Column(db.Float)

    def __repr__(self):
        return f"Diagnostics('{self.id}', '{self.test_name}', '{self.charge}')"


class PatientDiagnostics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer,db.ForeignKey('patient.id'))
    test_id = db.Column(db.Integer,db.ForeignKey('diagnostics.id'))
    ws_pat_name = db.Column(db.String(100), nullable=False)
    test_name = db.Column(db.String(100), nullable=False)
    charge = db.Column(db.Float)

    def __repr__(self):
        return f"PatientDiagnostics('{self.patient_id}'), '{self.test_id}')"

class Medicines(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    m_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Float)
    charge = db.Column(db.Float)

    def __repr__(self):
        return f"Medicines('{self.id}', '{self.m_name}', '{self.charge}')"


class PatientMedicine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer,db.ForeignKey('patient.id'))
    m_id = db.Column(db.Integer,db.ForeignKey('diagnostics.id'))
    ws_pat_name = db.Column(db.String(100), nullable=False)
    m_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Float)
    charge = db.Column(db.Float)

    def __repr__(self):
        return f"PatientDiagnostics('{self.patient_id}'), '{self.test_id}')"

