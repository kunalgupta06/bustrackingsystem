from flask import Flask, request, jsonify
import gpsd
import pygatt
from flask_migrate import Migrate
from flask import Flask, render_template, flash, request, redirect, url_for, session
from flask_wtf import FlaskForm 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Date
from flask_login import UserMixin, login_user, LoginManager,login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import ValidationError
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo
from flask import flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import pandas as pd
import PyPDF2
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from datetime import date
from wtforms.validators import DataRequired
from wtforms import HiddenField
from datetime import datetime
from dateutil import tz
app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///database.sqlite3"
app.app_context().push()
db =SQLAlchemy(app)
app.secret_key= 'secret_key'

migrate=Migrate(app,db)


class newuserlogin(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    firstname = db.Column(db.String(50),nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    _phone_number = db.Column("phone_number", db.String(50), nullable=False) 
    password = db.Column(db.String(50), nullable=False)
    confirm_password = db.Column(db.String(50), nullable=False)

    def validate_phone_number(self, key, phone_number):
        if len(phone_number) != 10 or not phone_number.isdigit():
            raise ValidationError('Phone number must be 10 digits')

    @property
    def phone_number(self):
        return self._phone_number

    @phone_number.setter
    def phone_number(self, value):
        self.validate_phone_number("_phone_number", value)
        self._phone_number = value
class userlogin(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(50),nullable=False)
    password = db.Column(db.String(50), nullable=False)

@app.route('/')
def home():
    return render_template('loginpage.html')

@app.route('/userlogin', methods=['GET', 'POST'])
def Userlogin():
    if request.method=='POST':
        username = request.form['Username']
        password = request.form['Password']
        
        user_data = userlogin.query.filter_by(username=username).first()
        

        if user_data and check_password_hash(user_data.password, password):
            
           return redirect(url_for('mainpage'))
        else:
           
            error_message = 'Invalid username or password'
            return render_template('loginpage.html', error_message=error_message)
    return render_template('loginpage.html', error_message=None)

@app.route('/newuser', methods=['GET', 'POST'])
def newuser1():
    if request.method == 'POST':
        first_name = request.form['First-Name']
        last_name = request.form['Last-Name']
        phone_number = request.form['Phone-Number']
        email = request.form['email']
        dob = request.form['DOB']
        username = request.form['Username']
        password = request.form['Password']
        confirm_password = request.form['Confirm-Password']

        if len(phone_number) != 10:
            error_message = 'Phone number must be 10 digits'
            return render_template('signup.html', error_message=error_message)

        if password != confirm_password:
            error_message = 'Passwords do not match'
            return render_template('signup.html', error_message=error_message)

        hashed_password = generate_password_hash(password)
        new_user_instance = newuserlogin(firstname=first_name,lastname=last_name, phone_number=phone_number, username=username, password=hashed_password, confirm_password=confirm_password,email=email,dob=dob)
        db.session.add(new_user_instance)
        db.session.commit()
        user_login_instance = userlogin(username=username, password=hashed_password)
        db.session.add(user_login_instance)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('Userlogin'))

    return render_template('signup.html', error_message=None)

@app.route('/mainpage')
def mainpage():
    return render_template('mainpage.html')
@app.route('/test')
def test():
    return render_template('livelocation.html')
@app.route('/busroute')
def busroute():
    return render_template('busroutes.html')


if __name__ == '__main__':
    
    app.run(debug=True)