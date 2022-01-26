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
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column , String , Integer
from datetime import datetime, timedelta
import uuid as uuid
import sys
from werkzeug.security import generate_password_hash , check_password_hash
from flask_login import LoginManager , UserMixin, login_user , login_required , logout_user , current_user
from werkzeug.utils import secure_filename
import os






#id generator

"""Pip installs:
pip install email_validator
pip install flask
pip install flask-bootstrap
pip install pandas
pip install flask-wtf
pip install flask_login
"""


app = Flask(__name__, template_folder = 'template')
app.config["SECRET_KEY"] = "Rahow3216"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///login.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
upload_folder = 'static/images/profilepics'
app.config['upload_folder'] = upload_folder
b(app)
db = SQLAlchemy(app)
IS_DEV = app.env == 'development'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index'


# def User1(username , password , email):
#     users_dict = {}
#     db = shelve.open('user.db', 'c')
#     try:
#         users_dict = db['Users']
#     except:
#         print("Error in retrieving Users from user.db.")
#     if username in users_dict:
#         print("invalid creditentials")
#     else:
#         users_dict[username] = {'password' : password , 'email' : email}
#         db['Users'] = users_dict
#         print(users_dict)
#         db.close()

class User(UserMixin,db.Model):
    __table_args__ = (
        db.UniqueConstraint('id', name='unique_component_commit'),
    )
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(80))
    gender = db.Column(db.String(6))
    profile_pic = db.Column(db.String(),nullable= True)



@login_manager.user_loader
def loaded(id_user):
    return User.query.get(int(id_user))

@app.route('/', methods = ['GET' , 'POST'])
def Home_Page():
    form2 = CreateUserForm()
    if form2.validate_on_submit():
        hash = generate_password_hash(form2.password.data , method = 'sha256')
        user_ID = int(id(form2.username.data))
        new_user = User(username = form2.username.data , email = form2.email.data , password = hash , gender = form2.gender.data , id = user_ID)
        db.session.add(new_user)
        db.session.commit()
        return '<h1> New user has been added! </h1>'
    forms = ExistingMember()
    if forms.validate_on_submit():
        user = User.query.filter_by(username = forms.username.data).first()
        if user:
            if check_password_hash(user.password , forms.password.data):
                login_user(user , remember = forms.remember.data)
                return render_template('index.html' , form1 = form2 , form = forms)
            return '<h1> Invalid username or password </h1>'
        # return '<h1>' + form1.username.data + " " + form1.password.data + "</h1>"
    return render_template('index.html' , form1 = form2 , form = forms)






   

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect('/')

@app.route('/dashboard/dist/dash.html' , methods = ['POST' , 'GET'])
def dash():
    form = CreateUserForm()
    name_to_update = User.query.get(current_user.id)
    if request.method == 'POST':
        # UPDATING USER INFORMATION
        name_to_update.username = request.form['username']
        name_to_update.email = request.form['email']
        name_to_update.profile_pic = request.files['profile_pic']

        pic_filename = secure_filename(name_to_update.profile_pic.filename)
        # pic_name = str(str(uuid.uuid1()) + "_" + str(pic_filename))

        # SAVING PICTURE INTO STATIC FILE
        saver = request.files['profile_pic']
        # name_to_update.profile_pic.save(os.path.join(app.config['upload_folder'])  , pic_filename)


        name_to_update.profile_pic = pic_filename
        try:
            db.session.commit()
            
            flash('User updated successfully')
            return render_template('dashboard/dist/dash.html' , name_to_update = name_to_update , form = form)
        except:
            flash('error')
            return render_template('dashboard/dist/dash.html' , name_to_update = name_to_update , form = form)
    else:
        return render_template('dashboard/dist/dash.html' , name_to_update = name_to_update , form = form)


@app.route('/sp/shopping/dist/index2.html')
def shopping():
    return render_template('/sp/shopping/dist/index2.html')
@app.route('/index.html')
def home():
    return render_template('index.html')
if __name__ == '__main__':
    os.environ['FLASK_ENV'] = 'development'
    db.create_all()
    app.run(debug = True)

