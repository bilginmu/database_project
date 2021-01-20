from flask import Flask, render_template, request, redirect, url_for
from flask_login import login_user,current_user,logout_user,login_required
import user as user_class# user classes
import databaseutilities as backend # database operations
from datetime import date 
from passlib.hash import pbkdf2_sha256 as hasher

comparison_stack = []
basket_stack = []
edi_stack = []
search_stack = []
###
# DELETE and UPDATE DRONES for SELLER
# DELETE and UPDATE USERs  
# SEARCH DIFFERENT ATTRIBUTES 
###
@login_required
def home_page():
    # get drones from database
    if request.method == "POST":
        if "search1" in request.form:
            searched_att = request.form["searchop"]
            searched = request.form["searched"]
            if (searched_att == "arease"):
                drones = backend._get_searched_drones_with_area(searched)
                global search_stack
                search_stack = drones
                return redirect(url_for('search'))
            elif (searched_att == "technologyse"):
                drones = backend._get_searched_drones_with_tech(searched)
                global search_stack
                search_stack = drones
                return redirect(url_for('search'))
            elif (searched_att == "typese"):
                drones = backend._get_searched_drones_with_type(searched)
                global search_stack
                search_stack = drones
                return redirect(url_for('search'))
        if "addbasket" in request.form:
            drones = backend._get_homepage_drones()
            index = int(request.form["addbasket"])
            basket_stack.append(drones[index-1])
            return redirect(url_for('basket'))
        elif "compare" in request.form:
            drones = backend._get_homepage_drones()
            index = int(request.form["compare"])
            comparison_stack.append(drones[index-1])
            return redirect(url_for('home_page'))
        elif  "edit" in request.form:
            drones = backend._get_homepage_drones_for_seller(current_user.username)
            index = int(request.form["edit"])
            edi_stack.append(drones[index-1])
            return redirect(url_for('edit'))
    elif request.method == "GET":
        # if there is not drone in database, show empty web page
        if not current_user.is_admin:
            drones = backend._get_homepage_drones()
        else:
            drones = backend._get_homepage_drones_for_seller(current_user.username)
        if drones is None:
            drones = []
        return render_template("home.html",drones=(drones))

@login_required
def search():
    return render_template("search.html",drone=search_stack)

@login_required
def new_drone():
    if request.method == 'POST':
        # get new drone data
        name = request.form['dname']
        weight = request.form['dweight']
        height = request.form['dheight']
        length = request.form['dlength']
        endurance = request.form['dendurance']
        area = request.form['darea']
        technology = request.form['dtechnology']
        price = request.form['dprice']
        dtype = request.form['type']
        photo = request.form['filename']
        if photo is not None:
            photo = "static/photos/" + photo
        else:
            photo = "/static/photos/noimage.png"
        # if button is clicked, add drone to database
        if request.form['addbutton'] == "add":
            backend._add_drone(photo,name,dtype,weight,height,length,endurance,technology,area,price,current_user.username)
            return redirect(url_for('home_page'))
    elif request.method == "GET":
        return render_template("newdrone.html")



@login_required
def comparison_drone():
    global comparison_stack
    if len(comparison_stack) > 2:        
        comparison_stack = []
    if request.method == 'POST':
        comparison_stack = []
        return redirect(url_for('home_page'))
    if not comparison_stack or len(comparison_stack) == 1:
        return render_template("comparisondummy.html")
    else:
        return render_template("comparison.html",drones=comparison_stack)
 

@login_required
def basket():
    global basket_stack
    # calculate total price of basket
    if basket_stack:
        price = backend._get_basket_price(basket_stack)
    else:
        price = 0
    if request.method == "POST":
        # remove from basket(pop from basket_stack list)
        if "removebasket" in request.form:
            index = int(request.form['removebasket'])
            basket_stack.pop(index-1)
            return redirect(url_for('basket'))
        elif "buy" in request.form:
            # add order 
            today = date.today()
            order_date = today.strftime("%B %d, %Y") 
            backend._add_order(current_user.username,price,"Unknown",order_date,"Waiting")
            # add orderline to database
            global basket_stack 
            for i in basket_stack:
                print (i[1])
                backend._add_orderline(i[1],current_user.username)         
            basket_stack = []
            return redirect(url_for('home_page'))
    return render_template("basket.html",drones=list(dict.fromkeys(basket_stack)),totprice=price)

#@login_required
#def update_user():
@login_required
def orders():
    orders_drone = backend.get_order_drones(current_user.username)
    return render_template("orders.html",orders=orders_drone)

@login_required
def account():
    if (request.method == "POST"):
        # submit button is clicked
        if ("submit-user" in request.form):
            # get data from forms
            name = request.form['uname']
            address = request.form['address']
            email = request.form['email']
            country = request.form['country']
            password = request.form['password']
            # update user according to its type
            if (not current_user.is_admin):
                backend._update_customer(current_user.username,name,password,country,current_user.area,email,address)
            if (current_user.is_admin):
                backend._update_seller(current_user.username,name,password,country,current_user.area,current_user.delivery_time,current_user.payment_method)
        # delete button is clicked
        if ("delete" in request.form):
            if (not current_user.is_admin):
                backend._delete_customer(current_user.username)
            if (current_user.is_admin):
                backend._delete_seller(current_user.username)       
        return redirect(url_for('logout'))
    elif (request.method == "GET"):
        user = backend._get_user(current_user.username)
        return render_template("account.html",user=user)

@login_required
def edit():
    
    
    if request.method == "POST":
        global edi_stack
        if edi_stack:
            global edi_stack
            drone1 = edi_stack.pop(0)
            price = request.form["price"]
            print ("hadi",drone1)
            #(photo,name,dtype,weight,height,length,endurance,technology,area,price):
            backend._update_drone(drone1[8],drone1[1],drone1[2],drone1[5],drone1[6],drone1[7],drone1[3],drone1[4],drone1[9],price)
        else:
            print ("empty")
            drone1 = []        
        return redirect(url_for('home_page'))
    elif request.method == "GET":
        global edi_stack
        if edi_stack:
            global edi_stack
            return render_template("edit.html",row=edi_stack[0])
        else:   
            return render_template("edit.html",row=[])
def registration():
    if request.method == "POST":
        # take input arguments from web page
        name = request.form['uname']
        address = request.form['address']
        email = request.form['email']
        country = request.form['country']
        username = request.form['username']
        password = request.form['password']
        area = request.form['type'] 
        account = request.form['type2']
        # do operations if button is clicked
        if request.form['rbutton'] == 'Rbutton':
            # add user to database according to account type: customer or seller
            if account == "Customer":
                backend._add_customer(username,name,password,country,area,email,address)
            if account == "Seller":
                payment_method = request.form['type3']
                print (payment_method)
                delivery_time = request.form['time']
                backend._add_seller(username,name,password,country,area,delivery_time,payment_method)
            return redirect(url_for('login_page'))
    else:
        return render_template("registration.html")



def login_page():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # get user as a class
        user = user_class.get_user(username)
        # verificition of password
        if user is not None:            
            if hasher.verify(password,user.password):
                login_user(user)
                return redirect(url_for('home_page')) # error!!! redirect         
    return render_template("login.html")


@login_required
def logout():
    global basket_stack
    global comparison_drone
    basket_stack = []
    comparison_drone = []
    logout_user()
    return render_template("logout.html")