from wtforms import StringField, RadioField, SelectField, TextAreaField, validators , PasswordField , BooleanField , EmailField, Form , SubmitField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField , FileAllowed, FileRequired
from wtforms.fields.simple import FileField, SubmitField

class CreateUserForm(FlaskForm):
    username = StringField('username' , [validators.Length(min=1 , max=15) , validators.DataRequired()])
    password = PasswordField('password' , [validators.Length(min=1 , max=100) , validators.DataRequired()])
    email = EmailField('Email' , [validators.Length(min = 5 , max = 100) , validators.DataRequired()])
    gender = RadioField('Gender', choices=[('F', 'Female'), ('M', 'Male'), ('O', 'Others')], default='None')
    profile_pic = FileField('PROFILE PIC')
    submit = SubmitField('Submit')


class ExistingMember(FlaskForm):
    username = StringField('username' , [validators.Length(min=1 , max=15) , validators.DataRequired()])
    password = PasswordField('password' , [validators.Length(min=8 , max = 100) , validators.DataRequired()])
    remember = BooleanField('Remember Me')


  
    


