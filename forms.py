from wtforms import StringField, RadioField, SelectField, TextAreaField, validators , PasswordField , BooleanField , Form , SubmitField
from wtforms import Form, SubmitField,IntegerField,FloatField,StringField,TextAreaField,validators
from flask_wtf import FlaskForm
from flask_wtf.file import FileField , FileAllowed, FileRequired
from wtforms.fields.simple import FileField, SubmitField

class CreateUserForm(FlaskForm):
    username = StringField('username' , [validators.Length(min=1 , max=15) , validators.DataRequired()])
    password = PasswordField('password' , [validators.Length(min=1 , max=100) , validators.DataRequired()])
    email = StringField('Email' , [validators.Length(min = 5 , max = 100) , validators.DataRequired()])
    gender = RadioField('Gender', choices=[('F', 'Female'), ('M', 'Male'), ('O', 'Others')], default='None')
    profile_pic = FileField('PROFILE PIC' , validators = [FileAllowed(['jpg' , 'png'])])
    phone_number = StringField('Phone Number' , [validators.Length(min=1 , max = 8) , validators.DataRequired()])
    submit = SubmitField('Submit')


class ExistingMember(FlaskForm):
    username = StringField('username' , [validators.Length(min=1 , max=15) , validators.DataRequired()])
    password = PasswordField('password' , [validators.Length(min=8 , max = 100) , validators.DataRequired()])
    remember = BooleanField('Remember Me')


class Addproducts(Form):
    name = StringField('Name', [validators.DataRequired()])
    price = FloatField('Price', [validators.DataRequired()])
    discount = IntegerField('Discount', default=0)
    stock = IntegerField('Stock', [validators.DataRequired()])
    colors = StringField('Colors', [validators.DataRequired()])
    discription = TextAreaField('Discription', [validators.DataRequired()])

    image_1 = FileField('Image 1', validators=[FileRequired(), FileAllowed(['jpg','png','gif','jpeg']), 'Images only please'])
    image_2 = FileField('Image 2', validators=[FileRequired(), FileAllowed(['jpg','png','gif','jpeg']), 'Images only please'])
    image_3 = FileField('Image 3', validators=[FileRequired(), FileAllowed(['jpg','png','gif','jpeg']), 'Images only please'])


  
    


