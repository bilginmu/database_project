from flask_login import UserMixin
import databaseutilities as backend
class customer(UserMixin):
    def __init__(self,username,name,password,country,area,email,address):
        self.username = username
        self.name = name
        self.password = password
        self.country = country
        self.area = area
        self.email = email
        self.address = address
        self.is_admin = False
        self.active = True
    def get_id(self):
        return self.username
    def is_active(self):
        return self.active

class seller(UserMixin):
    def __init__(self,username,name,password,country,area,delivery_time,payment_method):
        self.username = username 
        self.name = name 
        self.password = password
        self.country = country
        self.area = area
        self.delivery_time = delivery_time
        self.payment_method = payment_method
        self.is_admin = True
        self.active = True
    def get_id(self):
        return self.username
    def is_active(self):
        return self.active



def get_user(username):
    connection,cursor = backend.get_db()
    # if user is customer
    query = "SELECT * FROM customer WHERE username=%s"
    cursor.execute(query,(username,))
    user = cursor.fetchone()
    if user is not None:
        User = customer(user[0],user[1],user[2],user[3],user[4],user[5],user[6])
        backend.close_db(cursor)
        return User
    # if user is seller
    query = "SELECT * FROM seller WHERE username=%s"
    cursor.execute(query,(username,))
    user = cursor.fetchone()
    if user is not None:
        User = seller(user[0],user[1],user[2],user[3],user[4],user[5],user[6])
        backend.close_db(cursor)
        return User
    return None