from flask import Flask, render_template, request
from datetime import datetime


"""
    TO DO:
        Sort drones according to customer area
"""
drones = (("static/photos/crazyflie.jpeg","Skydiver", "Quad", "3", "10","20","30","racing","lidar","10"),
          ("static/photos/crazyflie.jpeg","Skydiver", "Quad", "3", "10","20","30","racing","lidar","10"),
          ("static/photos/crazyflie.jpeg","Skydiver", "Quad", "3", "10","20","30","racing","lidar","10"),
          ("static/photos/crazyflie.jpeg","Skydiver", "Quad", "3", "10","20","30","racing","lidar","10"))
droneatbasket = []
dronecomparison = []
dronecomparison.append(drones[0]) # dummy for first
dronecomparison.append(drones[1]) # dummy for first

def home_page():
    
    if request.method == "POST":
        
        index = int(request.form["addbasket"])
        print (index)
        global droneatbasket
        droneatbasket.append(drones[index-1])
        return render_template("droneatbasket.html")

    elif request.method == "GET":
        return render_template("home.html",drones=drones)
    

"""
    TO DO: 
        Add new drone to database   
"""
def new_drone():
    # get new drone data
    if request.method == "POST":
        dronename = request.form['dname']
        weight = request.form['dweight']
        height = request.form['dheight']
        length = request.form['dlength']
        endurance = request.form['dendurance']
        area = request.form['darea']
        technology = request.form['dtechnology']
        price = request.form['dprice']
        dronetype = request.form['type']
        # if button is clicked, return home page

        if request.form['addbutton'] == "add":
            return render_template("afterdroneadded.html")
    elif request.method == "GET":
        return render_template("newdrone.html")




"""
    TO DO: 
        Compare drones according to button at the home page
"""
def comparison_drone():
    return render_template("comparison.html",drones=dronecomparison)
 

def registration():
    # get datas from web page
    if request.method == "POST":
        
        name = request.form['uname']
        surname = request.form['sname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        area = request.form['type'] 
        account = request.form['type2']
        """
            TO BE ADDED: SEND THIS DATA to DATABASE
        """
        # direct the home page
        if request.form['rbutton'] == 'Rbutton':
            return home_page()
    else:
        return render_template("registration.html")

def basket():
    if request.method == "POST":
        index = int(request.form['removebasket'])
        droneatbasket.pop(index-1)
        render_template("basketafterremoved.html")
    return render_template("basket.html",drones=droneatbasket)
