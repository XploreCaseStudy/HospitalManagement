from flask_wtf import FlaskForm
from wtforms import StringField,FloatField,IntegerField, PasswordField,SelectField, SubmitField, BooleanField,DateField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired,Regexp, Length, Email, EqualTo, ValidationError
from HMD.models import User,Patient,Diagnostics,Medicines
from HMD import db


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    # email = StringField('Email',
    #                     validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    # def validate_email(self, email):
    #     user = User.query.filter_by(email=email.data).first()
    #     if user:
    #         raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class PatientForm(FlaskForm):
    ws_pat_name = StringField('Name',validators=[DataRequired(),Regexp('^[A-Za-z]')])
    ws_adrs = StringField('Address',validators=[DataRequired()])
    ws_age = StringField('Age',validators=[DataRequired(),Regexp('^[0-9]'), Length(min=2)])
    ws_doj = DateField('Date Of Joining',format='%d-%m-%Y')
    HOUR_CHOICES = [('1', 'General'), ('2', 'Semi'), ('3', 'Simple')]
    ws_rtype = SelectField('Room Type', choices=HOUR_CHOICES)
    submit = SubmitField('Submit')


class Up(FlaskForm):
    identity = IntegerField('identity',validators=[DataRequired()])
    submit = SubmitField('Submit')


class Done(FlaskForm):
    submit = SubmitField('Done')


class Search(FlaskForm):
    id = IntegerField('identity*',validators=[DataRequired()])
    ws_pat_name = StringField('Name',validators=[Regexp('^[A-Za-z]')])
    ws_adrs = StringField('Address')
    ws_age = StringField('Age',validators=[Regexp('^[0-9]'), Length(min=2)])
    ws_doj = DateField('Date Of Joining',format='%d-%m-%Y')
    HOUR_CHOICES = [('1', 'General'), ('2', 'Semi'), ('3', 'Simple')]
    ws_rtype = SelectField('Room Type', choices=HOUR_CHOICES)
    submit = SubmitField('Search')


class NewDForm(FlaskForm):
    dName = StringField('Diagnosis Name',validators=[DataRequired(),Regexp('^[A-Za-z]')])
    charge = FloatField('Charge',validators=[DataRequired()])
    submit = SubmitField('Submit')

class DiagnosisForm(FlaskForm):
    dname = QuerySelectField(query_factory=lambda: Diagnostics.query.all(),get_label='test_name')
    submit = SubmitField('Submit')


class NewMForm(FlaskForm):
    mName = StringField('Medicine Name:',validators=[DataRequired(),Regexp('^[A-Za-z]')])
    charge = FloatField('Charge',validators=[DataRequired()])
    quantity = FloatField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Submit')

class Clear(FlaskForm):
    Clean = SubmitField('Clear')

class MedicineForm(FlaskForm):
    mname = QuerySelectField(query_factory=lambda: Medicines.query.all(),get_label='m_name')
    quantity = FloatField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Submit')
