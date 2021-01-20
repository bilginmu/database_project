import psycopg2 as dbapi2
from passlib.hash import pbkdf2_sha256 as hasher
dsn = """dbname='dronedb' user='postgres'
         host='localhost' password='postgres'"""

# connect database
def get_db():
    connection = dbapi2.connect(dsn)
    cursor = connection.cursor()
    return connection,cursor
# close database
def close_db(cursor):
    cursor.close()

def init_db():
    _create_customer_table()
    _create_seller_table()
    _create_drone_table()
    _create_order_table()
    _create_orderline_table()


def _create_customer_table():
    connection,cursor = get_db()
    statement = """
        CREATE TABLE IF NOT EXISTS customer(
            username varchar(50) NOT NULL PRIMARY KEY,
            name varchar(50) NOT NULL,
            password varchar(500) NOT NULL,
            country varchar(50) NOT NULL,
            area varchar(50) NOT NULL,
            email varchar(150) NOT NULL,
            address varchar(500) NOT NULL        
        );
        """
    cursor.execute(statement)
    connection.commit()
    close_db(cursor)

def _create_seller_table():
    connection,cursor = get_db()
    statement = """
        CREATE TABLE IF NOT EXISTS seller(
            username varchar(50) NOT NULL PRIMARY KEY,
            name varchar(50) NOT NULL,
            password varchar(500) NOT NULL,
            country varchar(50) NOT NULL,
            area varchar(50) NOT NULL,
            delivery_time integer NOT NULL,
            payment_method varchar(50) NOT NULL
        );   
    """
    cursor.execute(statement)
    connection.commit()
    close_db(cursor)

def _create_drone_table():
    connection,cursor = get_db()
    statement = """
        CREATE TABLE IF NOT EXISTS drone(
            id SERIAL PRIMARY KEY,
            name varchar(50) NOT NULL UNIQUE,
            type varchar(100) NOT NULL,
            endurance float NOT NULL,
            technology varchar(250) NOT NULL,
            weight float NOT NULL,
            height float NOT NULL,
            length float NOT NULL,
            photo varchar(500) NOT NULL,
            area varchar(50) NOT NULL,
            price float NOT NULL,
            seller varchar(50) REFERENCES seller(username) ON DELETE CASCADE
        );
    """
    cursor.execute(statement)
    connection.commit()
    close_db(cursor)

def _create_order_table():
    connection,cursor = get_db()
    statement = """
        CREATE TABLE IF NOT EXISTS orders(
            id SERIAL PRIMARY KEY,
            total_price float NOT NULL,
            shipped_date varchar(150) NOT NULL,
            order_date varchar(150) NOT NULL,
            status varchar(100) NOT NULL,
            customer_username varchar(50) REFERENCES customer(username) ON DELETE CASCADE
        );    
    """
    cursor.execute(statement)
    connection.commit()
    close_db(cursor)


def _create_orderline_table():
    connection,cursor = get_db()
    statement = """
        CREATE TABLE IF NOT EXISTS orderline(
            id SERIAL PRIMARY KEY,
            order_id integer REFERENCES orders(id) ON DELETE CASCADE,
            drone_id integer REFERENCES drone(id) ON DELETE CASCADE
        );    
    """
    cursor.execute(statement)
    connection.commit()
    close_db(cursor)


# add customer to database
def _add_customer(username,name,password,country,area,email,address):
    connection,cursor = get_db() 
    query = """INSERT INTO customer (username,name,password,country,area,email,address)
            VALUES (%s,%s,%s,%s,%s,%s,%s);"""
    cursor.execute(query,(username,name,hasher.hash(password),country,area,email,address))
    connection.commit()
    close_db(cursor)


# add seller to database
def _add_seller(username,name,password,country,area,delivery_time,payment_method):
    connection,cursor = get_db()
    query = """INSERT INTO seller (username,name,password,country,area,delivery_time,payment_method)
            VALUES (%s,%s,%s,%s,%s,%s,%s);""" 
    cursor.execute(query,(username,name,hasher.hash(password),country,area,delivery_time,payment_method))
    connection.commit()
    close_db(cursor)

# add drone to database
def _add_drone(photo,name,dtype,weight,height,length,endurance,technology,area,price,seller):
    connection,cursor = get_db()
    query = """INSERT INTO drone (photo,name,type,weight,height,length,endurance,technology,area,price,seller)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
    cursor.execute(query,(photo,name,dtype,weight,height,length,endurance,technology,area,price,seller))
    connection.commit()
    close_db(cursor)

# add order to database
def _add_order(customer_id,total_price,shipped_date,order_date,status):
    connection,cursor = get_db()
    query = """INSERT INTO orders (customer_username,total_price,shipped_date,order_date,status) 
            VALUES (%s,%s,%s,%s,%s);"""
    cursor.execute(query,(customer_id,total_price,shipped_date,order_date,status))
    connection.commit()
    close_db(cursor)

# add orderline to database
def _add_orderline(dronename,current_username):
    drone_id = _get_drone_id(dronename)
    order_id = _get_order_id(current_username)
    connection,cursor = get_db()
    query = """ INSERT INTO orderline (order_id,drone_id)
            VALUES (%s,%s);"""
    cursor.execute(query,(order_id,drone_id))
    connection.commit()
    close_db(cursor)

# get drone id from database, drone name is primary key
def _get_drone_id(name):
    connection,cursor = get_db()
    query = "SELECT id FROM drone WHERE name=%s;"
    cursor.execute(query,(name,))
    drone_id = cursor.fetchone()
    close_db(cursor)
    return drone_id[0]


# get order id from database for current_user
def _get_order_id(current_username):
    connection,cursor = get_db()
    query = "SELECT MAX(id) FROM orders WHERE customer_username=%s;"
    cursor.execute(query,(current_username,))
    order_id = cursor.fetchone()
    close_db(cursor)
    return order_id[0]

def _get_user(current_username):
    connection,cursor = get_db()
    query = "SELECT * FROM customer WHERE username=%s"
    cursor.execute(query,(current_username,))
    user = cursor.fetchone()
    if user is not None:
        close_db(cursor)
        return user
    # if user is seller
    query = "SELECT * FROM seller WHERE username=%s"
    cursor.execute(query,(current_username,))
    user = cursor.fetchone()
    if user is not None:
        close_db(cursor)
        return user
    return None

# delete drone from database
def _delete_drone(name):
    connection,cursor = get_db()
    query = "DELETE FROM drone WHERE name=%s CASCADE;"
    cursor.execute(query,(name,))
    connection.commit()
    close_db(cursor)

# delete order from database
def _delete_order(current_username):
    connection,cursor = get_db()
    query = "DELETE FROM orders WHERE customer_username=%s CASCADE;"
    cursor.execute(query,(current_username,))
    connection.commit()
    close_db(cursor)

# delete customer from database
def _delete_customer(current_username):
    connection,cursor = get_db()
    query = "DELETE FROM customer WHERE username=%s;"
    cursor.execute(query,(current_username,))
    connection.commit()
    close_db(cursor)

# delete seller from database
def _delete_seller(current_username):
    connection,cursor = get_db()
    query = "DELETE FROM seller WHERE username=%s;"
    cursor.execute(query,(current_username,))
    connection.commit()
    close_db(cursor)


# update drone with name which is foreign key and you cannot update name
def _update_drone(photo,name,dtype,weight,height,length,endurance,technology,area,price):
    connection,cursor = get_db()
    query = """ UPDATE drone
        SET (photo,type,weight,height,length,endurance,technology,area,price)=(%s,%s,%s,%s,%s,%s,%s,%s,%s) 
        WHERE name=%s;"""
    cursor.execute(query,(photo,dtype,weight,height,length,endurance,technology,area,price,name))
    connection.commit()
    close_db(cursor)

# update customer with username which is foreign key and you cannot update username
def _update_customer(username,name,password,country,area,email,address):
    connection,cursor = get_db()
    query = """ UPDATE customer
        SET (name,password,country,area,email,address) = (%s,%s,%s,%s,%s,%s)
        WHERE username=%s;
        """
    cursor.execute(query,(name,hasher.hash(password),country,area,email,address,username))
    connection.commit()
    close_db(cursor)


# update seller with username which is foreign key and you cannot update username
def _update_seller(username,name,password,country,area,delivery_time,payment_method):
    connection,cursor = get_db()
    query = """ UPDATE seller
        SET (name,password,country,area,delivery_time,payment_method) = (%s,%s,%s,%s,%s,%s) 
        WHERE username=%s;
        """ 
    cursor.execute(query,(name,hasher.hash(password),country,area,delivery_time,payment_method,username))
    connection.commit()
    close_db(cursor)


# get homepage drones from database, drones are sorted according to its price
def _get_homepage_drones():
    connection,cursor = get_db()
    query = "SELECT * FROM drone ORDER BY price ASC;"
    cursor.execute(query)
    drones_ordered = cursor.fetchall()
    close_db(cursor)
    return drones_ordered
def _get_homepage_drones_for_seller(current_username):
    connection,cursor = get_db()
    query = "SELECT * FROM drone WHERE seller=%s ORDER BY price ASC;"
    cursor.execute(query,(current_username,))
    drones_homepage_for_seller = cursor.fetchall()
    close_db(cursor)
    return drones_homepage_for_seller

def get_order_drones(customer_username):
    drones =  _get_order_drones(customer_username)
    orders = []
    order = []
    for i in range(len(drones)-1):
        order.append(drones[i])
        if(drones[i][0] != drones[i+1][0]):
            orders.append(order)
            if(drones[i+1] == drones[-1]):
                order = []
                order.append(drones[-1])
                orders.append(order)
            order = []
        if(drones[i][0] == drones[i+1][0] and drones[i+1]==drones[-1]):
            order.append(drones[i+1])
            orders.append(order)
    return orders

def _get_order_drones(customer_username):
    connection,cursor = get_db()
    query = """SELECT or1.id,  cus.name, cus.address, d.name,d.price,or1.total_price 
        FROM orderline ol
        INNER JOIN orders as or1
        ON or1.id=ol.order_id
        INNER JOIN drone d
        ON d.id=ol.drone_id
        INNER JOIN customer cus
        ON cus.username=or1.customer_username
        WHERE cus.username=%s;
        """
    cursor.execute(query,(customer_username,))
    drones = cursor.fetchall()
    close_db(cursor)
    return drones

# get total price of drones from database
def _get_basket_price(drones):
    ids = []
    for i in drones:
        ids.append(i[0])
    connection,cursor = get_db()
    query = "SELECT SUM(price) FROM drone WHERE id in %s"
    cursor.execute(query,(tuple(ids),))
    total_price = cursor.fetchone()
    close_db(cursor)
    return total_price[0]

def _get_searched_drones_with_area(area):
    connection,cursor = get_db()
    query = """SELECT sel.username, sel.name, d.name, d.price, sel.payment_method 
        FROM drone d 
        INNER JOIN seller sel
        ON d.seller=sel.username
        WHERE d.area=%s;
        """
    cursor.execute(query,(area,))
    drones = cursor.fetchall()
    close_db(cursor)
    return drones
def _get_searched_drones_with_tech(tech):
    connection,cursor = get_db()
    query = """SELECT sel.username, sel.name, d.name, d.price, sel.payment_method 
        FROM drone d 
        INNER JOIN seller sel
        ON d.seller=sel.username
        WHERE d.technology=%s;
        """
    cursor.execute(query,(tech,))
    drones = cursor.fetchall()
    close_db(cursor)
    return drones

def _get_searched_drones_with_type(dtype):
    connection,cursor = get_db()
    query = """SELECT sel.username, sel.name, d.name, d.price, sel.payment_method 
        FROM drone d 
        INNER JOIN seller sel
        ON d.seller=sel.username
        WHERE d.type=%s;
        """
    cursor.execute(query,(dtype,))
    drones = cursor.fetchall()
    close_db(cursor)
    return drones
