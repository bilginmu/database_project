from flask import Flask, render_template, request, redirect, url_for
from flask_login import login_user,current_user,logout_user,login_required
import databaseutils as dbutils
from passlib.hash import pbkdf2_sha256 as hasher

drones = (("static/photos/crazyflie.jpeg","Skydiver", "Quad", "3", "10","20","30","racing","lidar","10"),
          ("static/photos/crazyflie.jpeg","Skydiver", "Quad", "3", "10","20","30","racing","lidar","10"),
          ("static/photos/crazyflie.jpeg","Skydiver", "Quad", "3", "10","20","30","racing","lidar","10"),
          ("static/photos/crazyflie.jpeg","Skydiver", "Quad", "3", "10","20","30","racing","lidar","10"))
droneatbasket = []
dronecomparison = []
dronecomparison.append(drones[0]) # dummy for first
dronecomparison.append(drones[1]) # dummy for first



@login_required
def home_page():
    if request.method == "POST":
        index = int(request.form["addbasket"])
        print (index)
        global droneatbasket
        droneatbasket.append(drones[index-1])
        return render_template("droneatbasket.html")

    elif request.method == "GET":
        return render_template("home.html",drones=drones)
    


@login_required
def new_drone():
    # get new drone data
    if request.method == 'POST':
        dronename = request.form['dname']
        weight = request.form['dweight']
        height = request.form['dheight']
        length = request.form['dlength']
        endurance = request.form['dendurance']
        area = request.form['darea']
        technology = request.form['dtechnology']
        price = request.form['dprice']
        dronetype = request.form['type']
        filename = request.form['filename']
        if filename == " ":
            pass
        else:
            filename = "noimage.png"
        # if button is clicked, return home page
        if request.form['addbutton'] == "add":
            return render_template("afterdroneadded.html")
    elif request.method == "GET":
        return render_template("newdrone.html")



@login_required
def comparison_drone():
    return render_template("comparison.html",drones=dronecomparison)
 

@login_required
def basket():
    if request.method == "POST":
        index = int(request.form['removebasket'])
        droneatbasket.pop(index-1)
        render_template("basketafterremoved.html")
    return render_template("basket.html",drones=droneatbasket)



def registration():
    if request.method == "POST":
        # take input arguments from html
        name = request.form['uname']
        address = request.form['address']
        email = request.form['email']
        country = request.form['country']
        username = request.form['username']
        password = request.form['password']
        area = request.form['type'] 
        account = request.form['type2']

        # create user according to account type: customer, distributor, company
        if account == "Customer":
            user = dbutils.customer(name,username,password,email,country,address,area)
        if account == "Distributor":
            payment_method = request.form['payment']
            delivery_time = request.form['time']
            user = dbutils.distriutor(name,username,password,email,country,area,payment_method,delivery_time)
        if account == "Company":
            print("company")
            user = dbutils.company(name,username,password,email,country,area)

        # redirect the login page
        if request.form['rbutton'] == 'Rbutton':
            user.insert_db() # added company to database
            return redirect(url_for('login_page'))
    else:
        return render_template("registration.html")



def login_page():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = dbutils.get_user(username)

        if user is not None:            
            if hasher.verify(password,user.password):
                login_user(user)
                return redirect(url_for('home_page')) # error!!! redirect 
                
    return render_template("login.html")

def logout():
    logout_user()
    return render_template("logout.html")