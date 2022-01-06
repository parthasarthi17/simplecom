from flask import Flask, request, render_template, redirect, jsonify, url_for, flash
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user, login_user, logout_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from sqlalchemy.sql import func
from sqlalchemy.orm import Session, relationship


from random import randint
import base64
import os
import pytz
import requests
import math


from init import app, db, api, migrate, login_manager, admin

from models.imagesmodel import Images
from models.productmodel import Product
from models.ratingmodel import productrating
from models.usermodel import User
from models.usercartmodel import usercart


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
        if current_user.vendor:
            f = request.files['file']
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))

            print(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))

            #newimage = imagesad(address = os.path.join(app.config['UPLOAD_FOLDER'], f.filename), filename = f.filename)
            new_name = request.form['productname']
            new_desc = request.form['productdesc']
            cat = request.form['category']
            brnd = current_user.brand
            newpr = request.form['price']
            disc = request.form['discount']

            newproduct = Product(p_name=new_name, description=new_desc, brand=brnd, category=cat, price=newpr, discount=disc, p_image_address=os.path.join(app.config['UPLOAD_FOLDER'], f.filename), p_image_name=f.filename)
            db.session.add(newproduct)
            db.session.commit()
        else:
            return "Not A Vendor!!"

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

    sold = db.session.query( db.func.sum(usercart.total).label('sumsoold')).filter(usercart.product_id==prod_id, usercart.status=="payed").first()[0]
    num_sold = db.session.query( db.func.sum(usercart.product_qty).label('numsold')).filter(usercart.product_id==prod_id, usercart.status=="payed").first()[0]
    xyz = xyz = db.session.query( db.func.avg(productrating.rating).label('totalrating')).filter(productrating.product_id==prod_id).first()[0]
    return render_template("productdetail.html", prod=prod, x=x, relatedp=relatedp, xyz = xyz, sold=sold, num_sold=num_sold)



@app.route('/mycart', methods=['GET', 'POST'])
def userscart():
    if current_user.is_authenticated:

        if request.method == 'POST':
            if request.form["prodqty"]:
                print(request.form["prodqty"])
                doesitexist = usercart.query.filter(usercart.product_id==request.form["productid"], usercart.person_id==current_user.id, usercart.status == "Shopping").first()
                print(doesitexist)

                productqnty = Product.query.filter_by(id = request.form["productid"]).first()

                if int(request.form["prodqty"])>productqnty.quantity_in_store:
                    return "Error, Cannot select more products than those currently available!!"
                else:
                    productqnty.quantity_in_store = productqnty.quantity_in_store - int(request.form["prodqty"])



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
        productqnty = Product.query.filter_by(id = prodid).first()
        print(float(request.form["newvalue"]))
        print(float(request.form["prevv"]))

        if float(request.form["newvalue"]) - float(request.form["prevv"])>productqnty.quantity_in_store:
            return "Error, Cannot select more products than those currently available!!"
        else:
            productqnty.quantity_in_store = productqnty.quantity_in_store - (float(request.form["newvalue"]) - float(request.form["prevv"]))
            db.session.commit()

        cartitems.product_qty = request.form["newvalue"]
        db.session.commit()
        return redirect(url_for("userscart"))

    else:
        return "current user not authenticated"


@app.route('/delete/<int:prodid>', methods=['POST', 'GET'])
def deletecart(prodid):
    if current_user.is_authenticated:
        cartitems = usercart.query.filter(usercart.person_id==current_user.id, usercart.status=="Shopping", usercart.product_id==prodid ).first()
        productqy = Product.query.filter_by(id = prodid).first()


        productqy.quantity_in_store = productqy.quantity_in_store + float(request.form["prevv"])
        db.session.commit()

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

                if current_user.is_vendor:
                    print(current_user.is_vendor)
                    print(current_user.is_authenticated)
                    print(current_user.vendor)
                    print('-------------------xx----------------')

                if current_user.vendor:
                    return redirect(url_for('vendhome'))

                else:
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

        print('---------------------------')

        print(current_user.is_authenticated)


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

##################################################################################################

@app.route('/registerasvendor', methods=['GET', 'POST'])
def registerasvendor():
    if request.method == 'POST':
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]
        brand = request.form["brand"]

        newuser = User(email = email, username = username, password=password, brand = brand, vendor = True)
        db.session.add(newuser)
        db.session.commit()

        result = User.query.filter_by(username=username).first()
        result.authenticated =True
        db.session.commit()
        print('asdsd')
        login_user(result)
        print(current_user.username)
        return redirect(url_for('vendhome'))


    return render_template('registervend.html')

@app.route('/vendor', methods=['GET', 'POST'])
def vendhome():
    if current_user.vendor:
        dataset = Product.query.filter_by(brand=current_user.brand).all()
    else:
        return redirect(url_for('home'))

    vendorproducts = Product.query.filter_by(brand=current_user.brand).all()
    earnings = 0
    for x in vendorproducts:
        if db.session.query( db.func.sum(usercart.total).label('sumsoold')).filter(usercart.product_id==x.id, usercart.status=="payed").first()[0] :
            earnings = earnings + db.session.query( db.func.sum(usercart.total).label('sumsoold')).filter(usercart.product_id==x.id, usercart.status=="payed").first()[0]

    return render_template("index.html", dataset=dataset, earnings = earnings)


@app.route('/vendorscart', methods=['GET', 'POST'])
def vendorscart():
    if current_user.is_authenticated:
        if current_user.vendor:
            vendorproducts = Product.query.filter_by(brand=current_user.brand).all()

            if request.method == 'POST':

                rpoductinq = Product.query.filter_by(id = request.form["prodid"]).first()

                rpoductinq.quantity_in_store = rpoductinq.quantity_in_store + float(request.form["Add"])

                db.session.commit()

                return redirect(url_for("vendorscart"))


            return render_template('vendorcart.html', vendorproducts=vendorproducts)
        else:
            return "not a vendor!"

    else:
        return "current user not authenticated"