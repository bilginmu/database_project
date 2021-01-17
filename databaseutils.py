import psycopg2 as dbapi2
from flask_login import UserMixin
from passlib.hash import pbkdf2_sha256 as hasher
dsn = """dbname='dronedb' user='postgres'
         host='localhost' password='postgres'"""



# Drone class for adding database
class drone:
    def __init__(self, photo,name,dtype, weight, height,length,endurance,area,technology,price):
        self.photo = photo
        self.name = name
        self.type = dtype
        self.weight = weight
        self.height = height
        self.length = length
        self.endurance = endurance
        self.area = area
        self.technology = technology
        self.price = price
    # insert database and get id of last inserted element 
    def insert_db(self):
        connection = dbapi2.connect(dsn)
        cursor = connection.cursor()
        query = """INSERT INTO drone (photo,name,type,weight,height,length,endurance,area,technology,price) VALUES 
                    (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
        cursor.execute(query,(self.photo,self.name,self.type,float(self.weight),float(self.height),float(self.length),float(self.endurance),self.area,self.technology,float(self.price)))
        connection.commit()
        #get id
        query = "SELECT CURRVAL('drone_id_seq')"
        cursor.execute(query)
        self.id = cursor.fetchone()
        

        cursor.close()



# USER CLASSES: customer, distributor, and company
class customer(UserMixin):
    def __init__(self,name,username,password,email,country,address,area):
        self.username = username
        self.password = password
        self.email = email
        self.country = country
        self.address = address
        self.name = name
        self.area = area
        self.account = "customer"
        self.active = True
        self.is_admin = False
        self.orders = None
    
    def get_id(self):
        return self.username
    def is_active(self):
        return self.active

    def insert_db(self):
        connection = dbapi2.connect(dsn)
        cursor = connection.cursor()
        query = """INSERT INTO CUSTOMER (name,email,username,password,country,address,area) VALUES 
                    (%s,%s,%s,%s,%s,%s,%s);"""
        cursor.execute(query,(self.name,self.email,self.username,hasher.hash(self.password),self.country,self.address,self.area))
        connection.commit()
        cursor.close()


class distriutor(UserMixin):
    def __init__(self,name,username,password,email,country,area,payment_method,delivery_time):
        self.username = username
        self.password = password
        self.email = email
        self.country = country
        self.name = name
        self.area = area
        self.payment_method = payment_method
        self.delivery_time = delivery_time
        self.account = "distributor"
        self.active = True
        self.is_admin = True
        self.drones = None

    def get_id(self):
        return self.username
    def is_active(self):
        return self.active

    def insert_db(self):
        connection = dbapi2.connect(dsn)
        cursor = connection.cursor()
        query = """INSERT INTO DISTRIBUTOR (name,email,country,username,password,area,PAYMENT_METHOD,DELIVERY_TIME,drone) VALUES 
                    (%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
        cursor.execute(query,(self.name,self.email,self.country,self.username,hasher.hash(self.password),self.area,self.payment_method,self.delivery_time,self.drones))
        connection.commit()
        cursor.close()

class company(UserMixin):
    def __init__(self,name,username,password,email,country,area):
        self.username = username
        self.password = password
        self.name = name
        self.email = email
        self.country = country
        self.area = area
        self.account = "company"
        self.active = True
        self.is_admin = True
        self.drones = None


    def get_id(self):
        return self.username
    def is_active(self):
        return self.active
    # insert user to database
    def insert_db(self):
        connection = dbapi2.connect(dsn)
        cursor = connection.cursor()
        query = """INSERT INTO COMPANY (name,email,username,password,country,area,drone) VALUES 
                    (%s,%s,%s,%s,%s,%s,%s);"""
        cursor.execute(query,(self.name,self.email,self.username,hasher.hash(self.password),self.country,self.area,self.drones))
        connection.commit()
        cursor.close()




# get user from user_id
def get_user(user_id):
    # find customer with given user name
    connection = dbapi2.connect(dsn)
    cursor = connection.cursor()

    # find if customer user
    query = "SELECT * FROM customer WHERE username=%s;"
    cursor.execute(query,(user_id,))
    user = cursor.fetchone()
    if user is not None:
        User = customer(user[0],user[2],user[3],user[0],user[4],user[5],user[6])
        User.drones = user[7]
        return User

    # find if distributor user
    query = "SELECT * FROM distributor WHERE username=%s;"
    cursor.execute(query,(user_id,))
    user = cursor.fetchone()
    if user is not None:
        User = distriutor(user[0],user[3],user[4],user[1],user[2],user[5],user[6],user[7])
        User.drones = user[8]
        return User
    
    # find if company user
    query = "SELECT * FROM company WHERE username=%s;"
    cursor.execute(query,(user_id,))
    user = cursor.fetchone()
    if user is not None:
        User = company(user[0],user[2],user[3],user[1],user[4],user[5])
        User.drones = user[6]
        return User

    cursor.close()
    return None
    



def add_drone(user,id_in):
    connection = dbapi2.connect(dsn)
    cursor = connection.cursor()
        
    if user.account == "company":
        query = "SELECT drone from company where username = %s"    
        cursor.execute(query,(user.username,))
        droneid = cursor.fetchone()
        # add drone if no drone exists in db
        if (droneid[0] == None):        
            query = "UPDATE company SET drone = %s where username = %s"
            cursor.execute(query,(id_in,user.username))
            connection.commit()
        # add drone if drone exists in db
        else:
            query = """INSERT INTO COMPANY (name,email,username,password,country,area,drone) VALUES 
                    (%s,%s,%s,%s,%s,%s,%s);"""
            cursor.execute(query,(user.name,user.email,user.username,hasher.hash(user.password),user.country,user.area,id_in))
            connection.commit()

    elif user.account == "distributor":
        query = "SELECT drone from distributor where username = %s"    
        cursor.execute(query,(user.username,))
        droneid = cursor.fetchone()
        # add drone if no drone exists in db
        if (droneid[0] == None):        
            query = "UPDATE distributor SET drone = %s where username = %s"
            cursor.execute(query,(id_in,user.username))
            connection.commit()
        # add drone if drone exists in db
        else:
            connection = dbapi2.connect(dsn)
            cursor = connection.cursor()
            query = """INSERT INTO DISTRIBUTOR (name,email,country,username,password,area,PAYMENT_METHOD,DELIVERY_TIME,drone) VALUES 
                        (%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
            cursor.execute(query,(user.name,user.email,user.country,user.username,hasher.hash(user.password),user.area,user.payment_method,user.delivery_time,id_in))
            connection.commit()
    cursor.close()

def get_drones():
    connection = dbapi2.connect(dsn)
    cursor = connection.cursor()
    query = "SELECT * FROM drone;"
    cursor.execute(query)
    drone = cursor.fetchone()
    drones = []
    while (drone is not None):
        drones.append(drone)
        drone = cursor.fetchone()

    cursor.close()
    return drones


    

