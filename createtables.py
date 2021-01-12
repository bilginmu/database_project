import psycopg2 as dbapi2
dsn = """dbname='dronedb' user='postgres'
         host='localhost' password='postgres'"""

connection = dbapi2.connect(dsn)
cursor = connection.cursor()
statement = "DROP TABLE DISTRIBUTOR"
cursor.execute(statement)
connection.commit()
statement = "DROP TABLE DRONE"
cursor.execute(statement)
connection.commit()


statement = """CREATE TABLE DRONE( ID SERIAL PRIMARY KEY,
    PRICE FLOAT NOT NULL,
    PHOTO VARCHAR(200) UNIQUE NOT NULL,
    TYPE VARCHAR(200) NOT NULL,
    ENDURANCE FLOAT NOT NULL,
    TECHNOLOGY VARCHAR(50),
    WEIGHT FLOAT NOT NULL,
    HEIGHT FLOAT NOT NULL,
    LENGTH FLOAT NOT NULL,
    AREA VARCHAR(50) NOT NULL
    )"""
cursor.execute(statement)
connection.commit()

statement = """ CREATE TABLE DISTRIBUTOR( USERNAME VARCHAR(20) PRIMARY KEY,
    PASSWORD VARCHAR(20) NOT NULL,
    NAME VARCHAR(20) NOT NULL,
    COUNTRY VARCHAR(20) NOT NULL,
    AREA VARCHAR(20) NOT NULL,
    PAYMENT_METHOD VARCHAR(20) NOT NULL,
    DELIVERY_TIME VARCHAR(20) NOT NULL,
    DRONE INTEGER REFERENCES DRONE (ID)
    )"""
cursor.execute(statement)
connection.commit()

statement = """CREATE TABLE COMPANY( USERNAME VARCHAR(20) PRIMARY KEY,
    PASSWORD VARCHAR(20) NOT NULL,
    NAME VARCHAR(20) NOT NULL,
    COUNTRY VARCHAR(20) NOT NULL,
    DRONE INTEGER REFERENCES DRONE (ID)
    )"""
cursor.execute(statement)
connection.commit()


statement = """CREATE TABLE ORDER( ID SERIAL PRIMARY KEY,
    PRICE FLOAT NOT NULL,
    STATUS VARCHAR(50) NOT NULL,
    SHIPPED_DATE VARCHAR(50) NOT NULL,
    REQUIRED_DATE VARCHAR(50) NOT NULL,
    ORDER_DATE VARCHAR(50) NOT NULL,
    DRONE INTEGER REFERENCES DRONE (ID) 
    )"""
cursor.execute(statement)
connection.commit()


statement = """CREATE TABLE CUSTOMER( USERNAME VARCHAR(50) PRIMARY KEY,
    PASSWORD VARCHAR(50) NOT NULL,
    NAME VARCHAR(50) NOT NULL,
    EMAIL VARCHAR(50) UNIQUE NOT NULL,
    COUNTRY VARCHAR(50) NOT NULL,
    ADDRESS VARCHAR(50) UNIQUE,
    AREA VARCHAR(50),
    ORDER INTEGER  REFERENCES ORDER (ID)
)"""
cursor.execute(statement)
connection.commit()

statement = """CREATE TABLE SELLER( SELLER_ID SERIAL PRIMARY KEY,
    COMPANY_ID INTEGER REFERENCES COMPANY (ID),
    DISTRIBUTOR_ID INTEGER REFERENCES COMPANY (ID)S
    )"""
cursor.execute(statement)
connection.commit()


cursor.close()

