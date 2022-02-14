from flask import Flask
from wtforms import StringField, RadioField, SelectField, TextAreaField, validators , PasswordField , BooleanField , Form , SubmitField
from wtforms import Form, SubmitField,IntegerField,FloatField,StringField,TextAreaField,validators
from flask_wtf import FlaskForm
from flask_wtf.file import FileField , FileAllowed, FileRequired
from wtforms.fields.simple import FileField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

class CreateUserForm(FlaskForm):
    username = StringField('username' , [validators.Length(min=1 , max=15) , validators.DataRequired()])
    password = PasswordField('password' , [validators.Length(min=1 , max=100) , validators.DataRequired()])
    email = StringField('Email' , [validators.Length(min = 5 , max = 100) , validators.DataRequired()])
    profile_pic = FileField('PROFILE PIC' , validators = [FileAllowed(['jpg' , 'png']) , validators.DataRequired()])
    phone_number = StringField('Phone Number' , [validators.Length(min=1 , max = 8) , validators.DataRequired()])
    submit = SubmitField('Submit')
    

class ExistingMember(FlaskForm):
    username = StringField('username' , [validators.Length(min=1 , max=15) , validators.DataRequired()])
    password = PasswordField('password' , [validators.Length(min=8 , max = 100) , validators.DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class Addproducts(Form):
    name = StringField('Name', [validators.DataRequired()])
    price = FloatField('Price', [validators.DataRequired()])
    discount = IntegerField('Discount', default=0)
    stock = IntegerField('Stock', [validators.DataRequired()])
    colors = StringField('Colors', [validators.DataRequired()])
    description = TextAreaField('Description', [validators.DataRequired()])
    stock = IntegerField('Stock', [validators.DataRequired()])
    image_1 = FileField('Image 1', validators=[FileRequired(), FileAllowed(['jpg','png','gif','jpeg'])])
    image_2 = FileField('Image 2', validators=[FileRequired(), FileAllowed(['jpg','png','gif','jpeg'])])
    image_3 = FileField('Image 3', validators=[FileRequired(), FileAllowed(['jpg','png','gif','jpeg'])])


class FeedbackForm(FlaskForm):
    name = StringField('Name', [validators.DataRequired()])
    email = StringField('Email' , [validators.Length(min = 5 , max = 100) , validators.DataRequired()])
    feedback = StringField('Feedback' , [validators.Length(min = 1 , max = 300) , validators.DataRequired])

class ShippingForm(FlaskForm):
    fname = StringField("First Name",validators=[DataRequired(), Length(min=1,max=255)])
    lname = StringField("Last Name",validators=[DataRequired(), Length(min=1,max=255)])
    address = StringField("Street Address",validators=[DataRequired()])
    addressl = StringField("Address Line 2",validators=[Optional()])
    city = StringField("City",validators=[DataRequired()])
    state = StringField("State",validators=[DataRequired()])
    zipcode = StringField("ZipCode",validators=[DataRequired()])
    submit = SubmitField("Next")

class Redeem(FlaskForm):
    code = StringField('coupon_code', [validators.DataRequired()])
