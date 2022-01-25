from flask import Flask, render_template, request , redirect , url_for , session , flash
import os
from flask.helpers import url_for
import pandas as pd
from sqlalchemy.sql.sqltypes import NullType
from wtforms import validators, Form
from forms import CreateUserForm , ExistingMember
from flask_wtf import FlaskForm
from wtforms import StringField , PasswordField, BooleanField , validators
from wtforms.validators import InputRequired , Email , Length 
from flask_bootstrap import Bootstrap as b
import shelve
from forms import CreateUserForm , ExistingMember
from flask_sqlalchemy import SQLAlchemy , inspect
from sqlalchemy import Column , String , Integer
from datetime import date
import uuid as uuid
import sys
from werkzeug.security import generate_password_hash , check_password_hash
from flask_login import LoginManager , UserMixin, login_user , login_required , logout_user , current_user
from werkzeug.utils import secure_filename
import os
import tkinter
from tkinter import messagebox
import PIL.Image as Image
from io import BytesIO
import io
import base64
from wtforms.validators import ValidationError

import string
import random
from datetime import datetime












#id generator

"""Pip installs:
pip install email_validator
pip install flask
pip install flask-bootstrap
pip install pandas
pip install pillow
pip install flask-wtf
"""


app = Flask(__name__, template_folder = 'template')

# creation of all database information
app.config["SECRET_KEY"] = "Rahow3216"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///login.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
b(app)
db = SQLAlchemy(app)

def Voucher(ID):
    voucher_dict = {}
    db = shelve.open('databases/voucher/voucher.db', 'c')
    try:
        voucher_dict = db['Voucher']
    except:
        print("Error in retrieving Users from user.db.")
    if ID in voucher_dict:
        print("voucher already generated")
    else:
        voucher_dict[ID] = {'value' : 10}
        db['voucher'] = voucher_dict
        db.close()





IS_DEV = app.env == 'development'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index'
upload_folder = 'static/images/profilepics'
app.config['upload_folder'] = upload_folder



ICON = (b'\x00\x00\x01\x00\x01\x00\x10\x10\x00\x00\x01\x00\x08\x00h\x05\x00\x00'
b'\x16\x00\x00\x00(\x00\x00\x00\x10\x00\x00\x00 \x00\x00\x00\x01\x00'
b'\x08\x00\x00\x00\x00\x00@\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
b'\x00\x01\x00\x00\x00\x01') + b'\x00'*1282 + b'\xff'*64
# base = ('R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==')




class User(UserMixin,db.Model):
    __table_args__ = (
        db.UniqueConstraint('id', name='unique_component_commit'),
    )
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(80))
    gender = db.Column(db.String(6))
    phone_number = db.Column(db.Integer() , unique = False)
    profile_pic = db.Column(db.LargeBinary, nullable= True , default = ICON)
    base64 = db.Column(db.String(64) , nullable = True , default = 'None' )
    date = db.Column(db.String(10) , unique = False , nullable = False)
    status = db.Column(db.Integer() , nullable = False , default = 'Enabled')
    admin = db.Column(db.Integer() , nullable = False , default = 'no')





# table = inspect(User)
# for column in table.c:
#     print(column.name)
# row = User.query.get('username')
# print(row)


@login_manager.user_loader
def loaded(id_user):
    return User.query.get(int(id_user))

@app.route('/', methods = ['GET' , 'POST'])
def Home_Page():
    form2 = CreateUserForm()
    if form2.validate_on_submit():
        hash = generate_password_hash(form2.password.data , method = 'sha256')
        user_ID = int(id(form2.username.data))
        user_by_name = User.query.filter_by(username=form2.username.data).first()
        if user_by_name:
            flash('username already taken')
        else:
            today = date.today()
            new_user = User(username = form2.username.data , email = form2.email.data , password = hash , gender = form2.gender.data , id = user_ID , phone_number = form2.phone_number.data , date = today.strftime("%d/%m/%Y"))
            db.session.add(new_user)
            db.session.commit()
            return '<h1> New user has been added! </h1>'
    forms = ExistingMember()
    if forms.validate_on_submit():
        user = User.query.filter_by(username = forms.username.data).first()
        if user:
            if check_password_hash(user.password , forms.password.data):
                login_user(user , remember = forms.remember.data)
                if user.status == 'Enabled':
                    return render_template('index.html' , form1 = form2 , form = forms)
                else:
                    return '<h1> your account has been disabled </h1>'
            return '<h1> invalid password </h1>'
        return '<h1> invalid username </h1>'
        # return '<h1>' + form1.username.data + " " + form1.password.data + "</h1>"
    return render_template('index.html' , form1 = form2 , form = forms)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect('/')

@app.route('/delete')
def delete():
    user_to_delete = User.query.filter_by(id = current_user.id).first()
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
    except:
        return redirect('/')
    return redirect('/')
    
@app.route('/dashboard/dist/dash.html' , methods = ['POST' , 'GET'])
def dash():
    form = CreateUserForm()
    name_to_update = User.query.get(current_user.id)
    users_table = User.query.all()
    
    if request.method == 'POST':
        # UPDATING USER INFORMATION
        name_to_update.username = request.form['username']
        name_to_update.email = request.form['email']

        #convert to bytes
        
        name_to_update.profile_pic = request.files['profile_pic'].read()
        

        base64_encoded_data = base64.b64encode(name_to_update.profile_pic)
        base64_message = base64_encoded_data.decode('utf-8')

        name_to_update.base64 = base64_message
        try:
            db.session.commit()
            flash('User updated successfully')
            return render_template('dashboard/dist/dash.html' , name_to_update = name_to_update , form = form , users_table = users_table)
        except:
            flash('error')
            return render_template('dashboard/dist/dash.html' , name_to_update = name_to_update , form = form , users_table = users_table)
    return render_template('dashboard/dist/dash.html' , name_to_update = name_to_update , form = form , users_table = users_table)
    
@app.route('/dashboard/dist/dash/enable/<int:id>' , methods = ['POST'])
@login_required
def user_enable(id):
    ID = User.query.filter_by(id = id).first()
    ID.status = 'Enabled'
    flash('Account ' + ID.username + ' has been unbanned' , category = 'success')
    db.session.commit()
    return redirect(url_for('dash'))

@app.route('/dashboard/dist/dash/disable/<int:id>' , methods = ['POST'])
@login_required
def user_disable(id):
    ID = User.query.filter_by(id = id).first()
    ID.status = 'Disabled'
    flash('Account ' + ID.username + ' has been banned' , category = 'danger')
    db.session.commit()
    return redirect(url_for('dash'))

@app.route('/dashboard/dist/dash/user_disable_admin/<int:id>' , methods = ['POST' , 'GET'])
@login_required
def user_disable_admin(id):
    ID = User.query.filter_by(id = id).first()
    ID.admin = 'no'
    db.session.commit()
    return redirect(url_for('dash'))

@app.route('/dashboard/dist/dash/user_enable_admin/<int:id>' , methods = ['POST' , 'GET'])
@login_required
def user_enable_admin(id):
    ID = User.query.filter_by(id = id).first()
    ID.admin = 'yes'
    db.session.commit()
    return redirect(url_for('dash'))

@app.route('/sp/shopping/dist/index2.html')
def shopping():
    return render_template('/sp/shopping/dist/index2.html')


@app.route('/index.html')
def home():
    forms = ExistingMember()
    form2 = CreateUserForm()
    return render_template('index.html' , form1 = form2 , form = forms)


@app.route('/updateuser/<int:id>' , methods = ['POST' , 'GET'])
@login_required
def updateuser(id):
    ID = User.query.filter_by(id=id).first()
    updateForm = CreateUserForm()

    if request.method == 'POST':
        ID.username = updateForm.username.data
        ID.email = updateForm.email.data
        db.session.commit()
        return redirect(url_for('dash'))
    if request.method == 'POST':
        return render_template('updateuser.html' , form = updateForm , user = ID)
    return render_template('updateuser.html' , form = updateForm , user = ID)


@app.route('/')
def index():
    return render_template('index.html')


# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feedback.db'
# db1 = SQLAlchemy(app)

# class Feedback(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(200), nullable = False)
#     date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Feedback('{self.name}')"












  


# @app.route('/use')
# def use():
#     # generatin of voucher code
#     S = 10  
#     IDGenerated = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S))
#     Voucher(IDGenerated) 
    

if __name__ == '__main__':
    os.environ['FLASK_ENV'] = 'development'
    db.create_all()
    app.run(debug = True)

