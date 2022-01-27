from re import S
from unicodedata import name
from flask import Flask, render_template, request , redirect , url_for , session , flash
import os
from flask.helpers import url_for
import pandas as pd
from sqlalchemy.sql.sqltypes import NullType
from wtforms import validators, Form
from forms import CreateUserForm , ExistingMember, ShippingForm
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
import os
import base64
from wtforms.validators import ValidationError
from datetime import datetime
from flask import render_template,session, request,redirect,url_for,flash,current_app
from forms import Addproducts
import secrets
import os
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_msearch import Search
from dataclasses import dataclass, field
from typing import Tuple
import pickle as pickle











#id generator

"""Pip installs:
pip install email_validator
pip install flask
pip install flask-bootstrap
pip install pandas
pip install pillow
pip install flask-wtf
pip install flask_login
"""


app = Flask(__name__, template_folder = 'template')

# creation of all database information
app.config["SECRET_KEY"] = "Rahow3216"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///login.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
b(app)
db = SQLAlchemy(app)

from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)



search = Search()
search.init_app(app)

migrate = Migrate(app, db)
with app.app_context():
    if db.engine.url.drivername == "sqlite":
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)

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
login_manager.login_message = u"Please login first"



ICON = (b'\x00\x00\x01\x00\x01\x00\x10\x10\x00\x00\x01\x00\x08\x00h\x05\x00\x00'
b'\x16\x00\x00\x00(\x00\x00\x00\x10\x00\x00\x00 \x00\x00\x00\x01\x00'
b'\x08\x00\x00\x00\x00\x00@\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
b'\x00\x01\x00\x00\x00\x01') + b'\x00'*1282 + b'\xff'*64
# base = ('R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==')



# user model
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

#product model
class Addproduct(db.Model):
    __seachbale__ = ['name','desc']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)
    discount = db.Column(db.Integer, default=0)
    stock = db.Column(db.Integer, nullable=False)
    colors = db.Column(db.Text, nullable=False)
    desc = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),nullable=False)
    category = db.relationship('Category',backref=db.backref('categories', lazy=True))

    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'),nullable=False)
    brand = db.relationship('Brand',backref=db.backref('brands', lazy=True))

    image_1 = db.Column(db.String(150), nullable=False, default='image1.jpg')
    image_2 = db.Column(db.String(150), nullable=False, default='image2.jpg')
    image_3 = db.Column(db.String(150), nullable=False, default='image3.jpg')

    def __repr__(self):
        return '<Post %r>' % self.name

# brand model
class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)

    def __repr__(self):
        return '<Brand %r>' % self.name
    
#category model
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)

    def __repr__(self):
        return '<Catgory %r>' % self.name

#shipping model
class ShippingInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=False, nullable=False)
    address = db.Column(db.String(255), unique=False, nullable=False)
    country = db.Column(db.String(50), unique=False, nullable=False)
    city = db.Column(db.String(50), unique=False, nullable=False)
    state = db.Column(db.String(50), unique=False, nullable=False)
    postalcode = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return '<ShippingInfo %r>' % self.name

#Customer Order

class JsonEcodedDict(db.TypeDecorator):
    impl = db.Text

    def set_value(self, value, dialect):
        if value is None:
            return '{}'
        else:
            return json.dumps(value)

    def get_value(self, value, dialect):
        if value is None:
            return {}
        else:
            return json



class CustomerOrder(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    invoice = db.Column(db.String(20),unique=True,nullable=False)
    status = db.Column(db.String,default='Pending',nullable=False)
    customer_id = db.Column(db.String,unique=False,nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    orders = db.Column(JsonEcodedDict)

    def __repr__(self):
        return '<CustomerOrder %r>' % self.invoice



@app.route('/admin')
def admin():
    products = Addproduct.query.all()
    return render_template('admin/index.html', title='Admin page',products=products)

@app.route('/brands')
def brands():
    brands = Brand.query.order_by(Brand.id.desc()).all()
    return render_template('admin/brand.html', title='brands',brands=brands)


@app.route('/categories')
def categories():
    categories = Category.query.order_by(Category.id.desc()).all()
    return render_template('admin/brand.html', title='categories',categories=categories)




@login_manager.user_loader
def loaded(id_user):
    return User.query.get(int(id_user))

@app.route('/index.html', methods = ['GET' , 'POST'])
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


@app.route('/')
def home1():
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



@app.route('/feedback.html')
def feedback():
    return render_template('feedback.html')


# end user login/register part


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable = False)
    email = db.Column(db.String(200), nullable = False)
    
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Feedback('{self.name}','{self.email})"




# feedback part stuff
@dataclass(order= True)
class Feedback:
    '''Object to store products'''
    _id : int
    _name : str
    _email : str 
    _feedback : str = field(compare= True, default= None) #sets default to null

    _sortID : int = field(init= False, repr= False)
    def __post_init__(self):
        object.__setattr__(self, '_sortID',  self._id)

    @property
    def id(self) -> int:
        return self._id
    @property
    def name(self) -> str:
        return self._name
    @property
    def email(self) -> str:
        return self._email
    @property
    def description(self) -> str:
        return self._feedback


def insertRow(name: str, email :str, feedback: str) -> None:
    with shelve.open('feedbackform') as db:
        if db: #if db is not empty
            id = int(list(db)[-1])+1
            db[str(id)] = Feedback(id, name, email, feedback)
        else: 
            db[str(1)] = Feedback(1, name, email, feedback)

def displayAllRows() -> None:
    with shelve.open('feedbackform') as db:
        for id, obj in db.items():
            print(f'{id=}, {obj}')

def getRow(id) -> Feedback:
    with shelve.open('feedbackform') as db:
        return db[str(id)]

def getAll() ->Tuple[Feedback]:
    with shelve.open('feedbackform') as db:
        return tuple(db.values())

def deleteRow(id : int) -> bool:
    try:
        with shelve.open('feedbackform') as db:
            del db[str(id)]
            return True
    except KeyError: 
        print(f'id of {id} is not inside database')
        return False

def deleteAll() -> bool: #is not imported with *
     with shelve.open('feedbackform') as db:
        try:
            for id in db.keys():
                del db[id]
            return True
        except KeyError: return False




# product page routes 

def brands():
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    return brands

def categories():
    categories = Category.query.join(Addproduct,(Category.id == Addproduct.category_id)).all()
    return categories



@app.route('/products/index.html')
def home():
    page = request.args.get('page',1, type=int)
    products = Addproduct.query.filter(Addproduct.stock > 0).order_by(Addproduct.id.desc()).paginate(page=page, per_page=8)
    return render_template('products/index.html', products=products,brands=brands(),categories=categories())

@app.route('/result')
def result():
    searchword = request.args.get('q')
    products = Addproduct.query.msearch(searchword, fields=['name','desc'] , limit=6)
    return render_template('products/result.html',products=products,brands=brands(),categories=categories())

@app.route('/product/<int:id>')
def single_page(id):
    product = Addproduct.query.get_or_404(id)
    return render_template('products/single_page.html',product=product,brands=brands(),categories=categories())




@app.route('/brand/<int:id>')
def get_brand(id):
    page = request.args.get('page',1, type=int)
    get_brand = Brand.query.filter_by(id=id).first_or_404()
    brand = Addproduct.query.filter_by(brand=get_brand).paginate(page=page, per_page=8)
    return render_template('products/index.html',brand=brand,brands=brands(),categories=categories(),get_brand=get_brand)


@app.route('/categories/<int:id>')
def get_category(id):
    page = request.args.get('page',1, type=int)
    get_cat = Category.query.filter_by(id=id).first_or_404()
    get_cat_prod = Addproduct.query.filter_by(category=get_cat).paginate(page=page, per_page=8)
    return render_template('products/index.html',get_cat_prod=get_cat_prod,brands=brands(),categories=categories(),get_cat=get_cat)


@app.route('/addbrand', methods=['GET','POST'])
def addbrand():
    if request.method == "POST":
        getbrand = request.form.get('brand')
        brand = Brand(name=getbrand)
        db.session.add(brand)
        flash(f'The brand {getbrand} was added to your database','success')
        db.session.commit()
        return redirect(url_for('addbrand'))
    return render_template('products/addbrand.html', title='Add brand',brands='brands')

@app.route('/updatebrand/<int:id>',methods=['GET','POST'])
def updatebrand(id):
    updatebrand = Brand.query.get_or_404(id)
    brand = request.form.get('brand')
    if request.method =="POST":
        updatebrand.name = brand
        flash(f'The brand {updatebrand.name} was changed to {brand}','success')
        db.session.commit()
        return redirect(url_for('brands'))
    brand = updatebrand.name
    return render_template('products/addbrand.html', title='Udate brand',brands='brands',updatebrand=updatebrand)


@app.route('/deletebrand/<int:id>', methods=['GET','POST'])
def deletebrand(id):
    brand = Brand.query.get_or_404(id)
    if request.method=="POST":
        db.session.delete(brand)
        flash(f"The brand {brand.name} was deleted from your database","success")
        db.session.commit()
        return redirect(url_for('admin'))
    flash(f"The brand {brand.name} can't be  deleted from your database","warning")
    return redirect(url_for('admin'))

@app.route('/addcat',methods=['GET','POST'])
def addcat():
    if request.method =="POST":
        getcat = request.form.get('category')
        category = Category(name=getcat)
        db.session.add(category)
        flash(f'The brand {getcat} was added to your database','success')
        db.session.commit()
        return redirect(url_for('addcat'))
    return render_template('products/addbrand.html', title='Add category')


@app.route('/updatecat/<int:id>',methods=['GET','POST'])
def updatecat(id):
    updatecat = Category.query.get_or_404(id)
    category = request.form.get('category')  
    if request.method =="POST":
        updatecat.name = category
        flash(f'The category {updatecat.name} was changed to {category}','success')
        db.session.commit()
        return redirect(url_for('categories'))
    category = updatecat.name
    return render_template('products/addbrand.html', title='Update cat',updatecat=updatecat)



@app.route('/deletecat/<int:id>', methods=['GET','POST'])
def deletecat(id):
    category = Category.query.get_or_404(id)
    if request.method=="POST":
        db.session.delete(category)
        flash(f"The brand {category.name} was deleted from your database","success")
        db.session.commit()
        return redirect(url_for('admin'))
    flash(f"The brand {category.name} can't be  deleted from your database","warning")
    return redirect(url_for('admin'))


@app.route('/products/addproduct.html', methods=['GET','POST'])
def addproduct():
    form = Addproducts(request.form)
    brands = Brand.query.all()
    categories = Category.query.all()
    if request.method=="POST"and 'image_1' in request.files:
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        colors = form.colors.data
        desc = form.discription.data
        brand = request.form.get('brand')
        category = request.form.get('category')
        image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
        image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
        image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
        addproduct = Addproduct(name=name,price=price,discount=discount,stock=stock,colors=colors,desc=desc,category_id=category,brand_id=brand,image_1=image_1,image_2=image_2,image_3=image_3)
        db.session.add(addproduct)
        flash(f'The product {name} was added in database','success')
        db.session.commit()
        return redirect(url_for('addproduct'))
    return render_template('products/addproduct.html', form=form, title='Add a Product', brands=brands,categories=categories)






@app.route('/updateproduct/<int:id>', methods=['GET','POST'])
def updateproduct(id):
    form = Addproducts(request.form)
    product = Addproduct.query.get_or_404(id)
    brands = Brand.query.all()
    categories = Category.query.all()
    brand = request.form.get('brand')
    category = request.form.get('category')
    if request.method =="POST":
        product.name = form.name.data 
        product.price = form.price.data
        product.discount = form.discount.data
        product.stock = form.stock.data 
        product.colors = form.colors.data
        product.desc = form.discription.data
        product.category_id = category
        product.brand_id = brand
        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/product" + product.image_1))
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
            except:
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/product" + product.image_2))
                product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
            except:
                product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
        if request.files.get('image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/product" + product.image_3))
                product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
            except:
                product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")

        flash('The product was updated','success')
        db.session.commit()
        return redirect(url_for('index'))
    form.name.data = product.name
    form.price.data = product.price
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.colors.data = product.colors
    form.discription.data = product.desc
    brand = product.brand.name
    category = product.category.name
    return render_template('products/addproduct.html', form=form, title='Update Product',getproduct=product, brands=brands,categories=categories)


@app.route('/deleteproduct/<int:id>', methods=['POST'])
def deleteproduct(id):
    product = Addproduct.query.get_or_404(id)
    if request.method =="POST":
        try:
            os.unlink(os.path.join(current_app.root_path, "static/product" + product.image_1))
            os.unlink(os.path.join(current_app.root_path, "static/product" + product.image_2))
            os.unlink(os.path.join(current_app.root_path, "static/product" + product.image_3))
        except Exception as e:
            print(e)
        db.session.delete(product)
        db.session.commit()
        flash(f'The product {product.name} was delete from your record','success')
        return redirect(url_for('admin'))
    flash(f'Can not delete the product','success')
    return redirect(url_for('admin'))






# add to cart routes/ stuff
def MagerDicts(dict1,dict2):
    if isinstance(dict1, list) and isinstance(dict2,list):
        return dict1  + dict2
    if isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))

@app.route('/addcart', methods=['POST'])
def AddCart():
    try:
        product_id = request.form.get('product_id')
        quantity = int(request.form.get('quantity'))
        color = request.form.get('colors')
        product = Addproduct.query.filter_by(id=product_id).first()

        if request.method =="POST":
            DictItems = {product_id:{'name':product.name,'price':float(product.price),'discount':product.discount,'color':color,'quantity':quantity,'image':product.image_1, 'colors':product.colors}}
            if 'Shoppingcart' in session:
                print(session['Shoppingcart'])
                if product_id in session['Shoppingcart']:
                    for key, item in session['Shoppingcart'].items():
                        if int(key) == int(product_id):
                            session.modified = True
                            item['quantity'] += 1
                else:
                    session['Shoppingcart'] = MagerDicts(session['Shoppingcart'], DictItems)
                    return redirect(request.referrer)
            else:
                session['Shoppingcart'] = DictItems
                return redirect(request.referrer)
              
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)



@app.route('/products/carts.html')
def getCart():
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    if len(session['Shoppingcart']) == 0:
        flash('Your shopping cart is empty' , category = 'danger')
    subtotal = 0
    grandtotal = 0
    for key,product in session['Shoppingcart'].items():
        discount = (product['discount']/100) * float(product['price'])
        subtotal += float(product['price']) * int(product['quantity'])
        subtotal -= discount
        tax =("%.2f" %(.06 * float(subtotal)))
        grandtotal = float("%.2f" % (1.06 * subtotal))
    return render_template('products/carts.html',tax=tax, grandtotal=grandtotal,brands=brands(),categories=categories())



@app.route('/updatecart/<int:code>', methods=['POST'])
def updatecart(code):
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    if request.method =="POST":
        quantity = request.form.get('quantity')
        color = request.form.get('color')
        try:
            session.modified = True
            for key , item in session['Shoppingcart'].items():
                if int(key) == code:
                    item['quantity'] = quantity
                    item['color'] = color
                    flash('Item is updated!' , 'success')
                    return redirect(url_for('getCart'))
        except Exception as e:
            print(e)
            return redirect(url_for('getCart'))



@app.route('/deleteitem/<int:id>')
def deleteitem(id):
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    try:
        session.modified = True
        for key , item in session['Shoppingcart'].items():
            if int(key) == id:
                session['Shoppingcart'].pop(key, None)
                return redirect(url_for('getCart'))
    except Exception as e:
        print(e)
        return redirect(url_for('getCart'))


@app.route('/clearcart')
def clearcart():
    try:
        session.pop('Shoppingcart', None)
        return redirect(url_for('home'))
    except Exception as e:
        print(e)






@app.route("/indexs.html", methods=["GET","POST"])
def indexs():
    return render_template("indexs.html")



@dataclass(order= True)
class Feedback:
    '''Object to store products'''
    _id : int
    _name : str
    _email : str 
    _feedback : str = field(compare= True, default= None) #sets default to null

    _sortID : int = field(init= False, repr= False)
    def __post_init__(self):
        object.__setattr__(self, '_sortID',  self._id)

    @property
    def id(self) -> int:
        return self._id
    @property
    def name(self) -> str:
        return self._name
    @property
    def email(self) -> str:
        return self._email
    @property
    def description(self) -> str:
        return self._feedback


def insertRow(name: str, email :str, feedback: str) -> None:
    with shelve.open('feedbackform') as db:
        if db: #if db is not empty
            id = int(list(db)[-1])+1
            db[str(id)] = Feedback(id, name, email, feedback)
        else: 
            db[str(1)] = Feedback(1, name, email, feedback)

def displayAllRows() -> None:
    with shelve.open('feedbackform') as db:
        for id, obj in db.items():
            print(f'{id=}, {obj}')
        return db.items()

def getRow(id) -> Feedback:
    with shelve.open('feedbackform') as db:
        return db[str(id)]

def getAll() ->Tuple[Feedback]:
    with shelve.open('feedbackform') as db:
        return tuple(db.values())

def deleteRow(id : int) -> bool:
    try:
        with shelve.open('feedbackform') as db:
            del db[str(id)]
            return redirect('dash')
    except KeyError: 
        print(f'id of {id} is not inside database')
        return redirect('dash')

def deleteAll() -> bool: #is not imported with *
    with shelve.open('feedbackform') as db:
        try:
            for id in db.keys():
                del db[id]
            return True
        except KeyError: return False

if __name__ == '__main__':
    # print(deleteAll())
    displayAllRows()
__all__ = ['Feedback', 'insertRow', 'displayAllRows', 'deleteRow', 'getRow', 'getAll']

@app.route('/indexs', methods=["POST"])
def form():
    firstname = request.form.get("firstname")
    email = request.form.get("lastname")
    subject = request.form.get("subject")
    insertRow(firstname,email,subject)
    flash('Thank you for your feedback' , 'success')
    return render_template("indexs.html")

@app.route('/displayFeedback')
def displayFeedback():
    feedback_table = getAll()
    return render_template('/displayFeedback.html' , feedback_table = feedback_table)

@app.route('/deleteFeedback/<int:id>')
def deleteFeedback(id):
    deleteRow(id)
    flash("Feedback has been deleted" , 'success')
    return redirect(url_for('displayFeedback'))

@app.route('/deleteAllFeedback')
def deleteAllFeedback():
    deleteAll()
    flash('All Feedback has been deleted' , 'success')
    return redirect(url_for('dash'))


#Transaction
@app.route("/shipping")
def shipping():
    form = ShippingForm(request.form)
    render_template("shipping.html",form=form)

@app.route('/checkout',methods=['POST'])
def checkout():
    form = ShippingForm(request.form)
    if request.method == 'POST':
        name = form.name.data
        address = form.address.data
        country = form.country.data
        city = form.city.data
        state = form.state.data
        zipcode = form.zipcode.data
        biling = ShippingInfo(name=name,address=address,country=country,city=city,state=state,postalcode=zipcode)
        db.session.add(biling)
        invoice = secrets.token_hex(5)
        try:
            order = CustomerOrder(invoice=invoice,customer_id=current_user.id,orders=session['Shoppingcart'])
            db.session.add(order)
            db.session.commit()
            return redirect(url_for('check_out',invoice=invoice))
        except Exception as e:
            print(e)
            return redirect(url_for('home'))

@app.route('/checkout/<invoice>')
def check_out(invoice):
    grandTotal = 0
    subTotal = 0
    customer = ShippingInfo.query.filter_by(name=current_user.__name).first()
    orders = CustomerOrder.query.filter_by(id=current_user.id).first()
    for key,product in session['Shoppingcart'].items():
        discount = (product['discount']/100) * float(product['price'])
        subTotal += float(product['price']) * int(product['quantity'])
        subTotal -= discount
        tax =("%.2f" %(.06 * float(subTotal)))
        grandtotal = float("%.2f" % (1.06 * subTotal))

    return render_template('checkout.html',customer=customer,orders=orders,grandTotal=grandTotal,subTotal=subTotal,tax=tax)







