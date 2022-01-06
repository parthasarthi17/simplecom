from flask import Flask, request, render_template, redirect, jsonify, url_for, flash
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user, login_user, logout_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from sqlalchemy.sql import func
from sqlalchemy.orm import Session, relationship
from flask_caching import Cache


from random import randint
import base64
import os
import pytz
import requests
import math


app = Flask(__name__)
db = SQLAlchemy(app)
api = Api(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
admin = Admin(app, name='Ecom', template_mode='bootstrap3')


app.config['CACHE_TYPE'] = "SimpleCache"
cache = Cache(app)

app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Tajhotels54321@localhost/ecom'
app.secret_key = 'some key'

app.config['UPLOAD_FOLDER'] = 'static/imagesfolder'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}



########################################################################################################################


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(25))
    username = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(15))
    user_city = db.Column(db.String(25))
    user_address = db.Column(db.String(50))
    authenticated = db.Column(db.Boolean, default=False)
    userpoints = db.Column(db.Integer)
    cart = db.relationship('usercart', backref='user', lazy=True)
    rate_products = db.relationship('productrating', backref='user', lazy='dynamic')

    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False


class usercart(db.Model):
    __tablename__ = 'usercart'
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'),nullable=False)
    product_qty = db.Column(db.Float)
    total = db.Column(db.Float)
    status = db.Column(db.String(40), default = "Shopping")


class productrating(db.Model):
    __tablename__ = 'productrating'
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'),nullable=False)


class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    p_name = db.Column(db.String(50))
    description = db.Column(db.String(500))
    p_image_address = db.Column(db.String(125), nullable = True)
    p_image_name = db.Column(db.String(125), nullable = True)
    brand = db.Column(db.String(50), nullable = True)
    category = db.Column(db.String(50))
    price = db.Column(db.Integer)
    discount = db.Column(db.Integer)
    speaicaloffer = db.Column(db.Boolean, default=False)
    cart = db.relationship('usercart', backref='product', lazy=True)
    ratings = db.relationship('productrating', backref='product', lazy='dynamic')
    no_ratings = db.Column(db.Integer, default = 0)
    avg_rating = db.Column(db.Float, nullable = True)

########################################################################################################################

class Images(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(120), nullable=False)
    data  = db.Column(db.LargeBinary )



########################################################################################################################
########################################################################################################################

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)

########################################################################################################################
########################################################################################################################

class MyModelView(ModelView):
    def is_accessible(self):
        return True


admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Product, db.session))
admin.add_view(MyModelView(usercart, db.session))
admin.add_view(MyModelView(Images, db.session))
admin.add_view(MyModelView(productrating, db.session))

########################################################################################################################
########################################################################################################################


u_args = reqparse.RequestParser()
u_args.add_argument("email", type=str, help = "dfsdf")
u_args.add_argument("username", type=str, help = "asd")
u_args.add_argument("password", type=str, help = "dfsasjdhasddf")
u_args.add_argument("email", type=str, help = "dfsdf")
u_args.add_argument("user_city", type=str, help = "asddas")
u_args.add_argument("user_address", type=str, help = "dsadasdasd")
u_args.add_argument("userpoints", type=int, help = "dfsdf")
u_args.add_argument("email", type=str, help = "dfsdf")
u_args.add_argument ("authenticated", type=bool, help = "sdiohaf")


user_fields ={
    'email':fields.String,
    'username':fields.String,
    'password':fields.String,
    'authenticated':fields.Boolean,
}


########################################################################################################################
########################################################################################################################

#login API, not required for user side!

class Login(Resource):
    @marshal_with(user_fields)
    def post(self):

        args = u_args.parse_args()
        test_username=args['username']
        test_password=args['password']

        result = User.query.filter_by(username=test_username).first()

        if result:
            print('sdfsdf')

            if result.password == test_password:
                print(result.email)
                result.authenticated =True
                db.session.commit()
                print('asdsd')
                login_user(result)
                print(current_user.username)
                return result
            else:
                return 'Incorrect Password!'

        else:
            return 'The username does not exist!'

api.add_resource(Login, "/login")

class Logout(Resource):
    @marshal_with(user_fields)
    def post(self):
        print(current_user)
        result = current_user
        result.authenticated = False
        logout_user()
        db.session.commit()

        return jsonify({"message":"loggedout"})

api.add_resource(Logout, "/logout")

########################################################################################################################
########################################################################################################################


##temporaryfor logging in dummy users

@app.route('/loginadmin', methods=['GET'])
def loginadmin():
    print(current_user)
    print('------------------------------------------------')
    result = User.query.filter_by(username='admin').first()
    result.authenticated =True
    db.session.commit()
    login_user(result)
    print(current_user.username)

    return 'result'

@app.route('/logoutadmin', methods=['GET'])
def logoutadmin():

    result = current_user
    result.authenticated =False
    db.session.commit()
    logout_user()
    return "logged out admin"

########################################################################################################################




@app.route('/uploadproducts', methods=['GET', 'POST'])
def uploadproducts():
    if request.method == 'POST':
        f = request.files['file']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))

        print(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))

        #newimage = imagesad(address = os.path.join(app.config['UPLOAD_FOLDER'], f.filename), filename = f.filename)
        new_name = request.form['productname']
        new_desc = request.form['productdesc']
        cat = request.form['category']
        brnd = request.form['brand']
        newpr = request.form['price']
        disc = request.form['discount']

        newproduct = Product(p_name=new_name, description=new_desc, brand=brnd, category=cat, price=newpr, discount=disc, p_image_address=os.path.join(app.config['UPLOAD_FOLDER'], f.filename), p_image_name=f.filename)
        db.session.add(newproduct)
        db.session.commit()
    return render_template('uploadimage.html')

@app.route('/allproducts', methods=['GET', 'POST'])
def allproducts():
    print(current_user.username)
    print('------------------------------------------------')

    dataset = Product.query.all()

    return render_template("allproducts.html", dataset=dataset)

@app.route('/cat/<string:catname>', methods=['GET', 'POST'])
def catsort(catname):
    print(catname)
    dataset = Product.query.filter(Product.category==catname).all()

    return render_template("catfilter.html", dataset=dataset, catname=catname)

@app.route('/brand/<string:bname>', methods=['GET', 'POST'])
def brndsort(bname):
    print(bname)
    dataset = Product.query.filter_by(brand=bname).all()
    print('--------------')
    print(dataset)


    return render_template("brndfilter.html", dataset=dataset, bname=bname)


@app.route('/', methods=['GET', 'POST'])
def home():
    dataset = Product.query.filter_by(speaicaloffer=True).all()
    return render_template("index.html", dataset=dataset)

@app.route('/popular', methods=['GET', 'POST'])
def populr():

    dataset = Product.query.filter(Product.avg_rating >= 4.0).all()

    return render_template("popular.html", dataset=dataset)



@app.route('/productdet/<int:prod_id>', methods=['GET', 'POST'])
def prodd(prod_id):
    prod = Product.query.filter_by(id=prod_id).first()
    print(prod.no_ratings)
    xcat = prod.category

    relatedp = Product.query.filter(Product.id!=prod_id, Product.category==xcat).all()
    print(relatedp)
    print('---------------------------------------------------')
    if request.method == 'POST':
        if request.form["Submitrating"]:
            doesitexist = productrating.query.filter_by(user_id=current_user.id, product_id=prod_id).first()
            if doesitexist:
                doesitexist.rating = request.form["userrating"]
                db.session.commit()
                x= doesitexist.rating
            else:
                newrating = productrating(user_id=current_user.id, product_id=prod_id, rating = request.form["userrating"])
                db.session.add(newrating)
                prod.no_ratings = prod.no_ratings + 1
                db.session.commit()
                x=request.form["userrating"]
            print(db.session.query( db.func.avg(productrating.rating).label('totalrating')).filter(productrating.product_id==prod_id).first()[0])
            xyz = db.session.query( db.func.avg(productrating.rating).label('totalrating')).filter(productrating.product_id==prod_id).first()[0]

            print('-------------------------')
            print(xyz)
            print('-------------------------')
            prod.avg_rating  = xyz
            print(prod.avg_rating)
            print('--------------------------------=============------------')
            db.session.commit()

            return redirect(f'/productdet/{prod_id}')


        return render_template("productdetail.html", prod=prod, x=x, relatedp=relatedp)

    if current_user.is_authenticated:
        doesitexist = productrating.query.filter_by(user_id=current_user.id, product_id=prod_id).first()
        if doesitexist:
            x= doesitexist.rating
            print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
            print(x)
        else:
            x=0
    else:
        x=0
    xyz = xyz = db.session.query( db.func.avg(productrating.rating).label('totalrating')).filter(productrating.product_id==prod_id).first()[0]
    return render_template("productdetail.html", prod=prod, x=x, relatedp=relatedp, xyz = xyz)



@app.route('/mycart', methods=['GET', 'POST'])
def userscart():
    if current_user.is_authenticated:

        if request.method == 'POST':
            if request.form["prodqty"]:
                print(request.form["prodqty"])
                doesitexist = usercart.query.filter(usercart.product_id==request.form["productid"], usercart.person_id==current_user.id, usercart.status == "Shopping").first()
                print(doesitexist)
                xiid = request.form["productid"]
                p_added = Product.query.filter_by(id=xiid).first()

                print('--------------------------------------------')
                print(xiid)
                print('--------------------------------------------')
                print(request.form["prodqty"])

                p_price = (p_added.price*((100-p_added.discount)/100))

                print('--------------------------------------------')
                print(p_price)
                totalprice = float(request.form["prodqty"])*p_price
                print(totalprice)


                if doesitexist:
                    doesitexist.product_qty = doesitexist.product_qty + float(request.form["prodqty"])
                    doesitexist.total = p_price*doesitexist.product_qty
                    db.session.commit()
                    print('++++++++++++++++++++++++++++++++++++++++++++++++')
                else:
                    newcart = usercart(person_id=current_user.id, product_id=request.form["productid"], product_qty = request.form["prodqty"], total = totalprice )
                    db.session.add(newcart)
                    db.session.commit()
                    print('-------------------------------------------------')

                return redirect(url_for('userscart'))

        cartitems = usercart.query.filter(usercart.person_id==current_user.id, usercart.status=="Shopping").all()

        print('===================================================================')

        print(cartitems)
        if not cartitems:
            return "No Items in Your cart currently!"
        total_cost = db.session.query( db.func.sum(usercart.total).label('totalcost')).filter(usercart.person_id==current_user.id, usercart.status=="Shopping").first()[0]

        return render_template("cart.html", cartitems=cartitems, total_cost=total_cost)
    else:
        return "current user not authenticated"

@app.route('/mytr', methods=['GET'])
def transactions():
    if current_user.is_authenticated:

        cartitems = usercart.query.filter(usercart.person_id==current_user.id, usercart.status=="payed").all()
        if not cartitems:
            return "No Items bought!"
        total_cost = db.session.query( db.func.sum(usercart.total).label('totalcost')).filter(usercart.person_id==current_user.id, usercart.status=="payed").first()[0]

        return render_template("transactions.html", cartitems=cartitems, total_cost=total_cost)
    else:
        return "current user not authenticated"





@app.route('/updatecart/<int:prodid>', methods=['POST', 'GET'])
def updcart(prodid):
    if current_user.is_authenticated:
        cartitems = usercart.query.filter(usercart.person_id==current_user.id, usercart.status=="Shopping", usercart.product_id==prodid ).first()
        print(cartitems)
        print('---------------------')
        cartitems.product_qty = request.form["newvalue"]
        db.session.commit()
        return redirect(url_for("userscart"))

    else:
        return "current user not authenticated"


@app.route('/delete/<int:prodid>', methods=['POST', 'GET'])
def deletecart(prodid):
    if current_user.is_authenticated:
        cartitems = usercart.query.filter(usercart.person_id==current_user.id, usercart.status=="Shopping", usercart.product_id==prodid ).first()
        print(cartitems)
        print('---------------------')
        db.session.delete(cartitems)
        db.session.commit()
        return redirect(url_for("userscart"))

    else:
        return "current user not authenticated"


@app.route('/checkoutusercart', methods=['GET', 'POST'])
def checkoutusercart():
    if current_user.is_authenticated:
        cartitems = usercart.query.filter(usercart.person_id==current_user.id, usercart.status=="Shopping").all()


        #for x in cartitems:
        #    x.status = "Payed"


        if not cartitems:
            return "No Items in Your cart currently!"

        else:
            spent =  db.session.query( db.func.sum(usercart.total).label('totalcost')).filter(usercart.person_id==current_user.id, usercart.status=="Shopping").first()[0]
            bonus = spent/20

            current_user.userpoints = current_user.userpoints - spent + bonus
            db.session.commit()

            for x in cartitems:
                 x.status = "payed"
                 db.session.commit()

            flash(f'You received cashback!!')
            return redirect(url_for('home'))

    else:
        return "current user not authenticated"


########################################################################################################################
@app.route('/loginuser', methods=['GET', 'POST'])
def loginuser():
    if request.method == 'POST':
        test_username = request.form["test_username"]
        test_password = request.form["test_password"]
        result = User.query.filter_by(username=test_username).first()

        if result:
            print('sdfsdf')

            if result.password == test_password:
                print(result.email)
                result.authenticated =True
                db.session.commit()
                print('asdsd')
                login_user(result)
                print(current_user.username)
                return redirect(url_for('home'))
            else:
                return 'Incorrect Password!'

        else:
            return 'The username does not exist!'

    return render_template('login.html')

@app.route('/logoutuser', methods=['GET', 'POST'])
def logoutuser():
        print(current_user)
        result = current_user
        result.authenticated = False
        logout_user()
        db.session.commit()

        return redirect(url_for('home'))

@app.route('/registeruser', methods=['GET', 'POST'])
def registeruser():
    if request.method == 'POST':
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]
        user_city = request.form["user_city"]
        user_address = request.form["user_address"]

        newuser = User(email = email, username = username, password=password, user_city=user_city, user_address=user_address, userpoints = 550)
        db.session.add(newuser)
        db.session.commit()

        result = User.query.filter_by(username=username).first()
        result.authenticated =True
        db.session.commit()
        print('asdsd')
        login_user(result)
        print(current_user.username)
        return redirect(url_for('home'))


    return render_template('registeruser.html')



########################################################################################################################


if __name__ =="__main__":
    app.run(debug=True, host='localhost', port=8000)
