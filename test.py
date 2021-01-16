import psycopg2 as dbapi2
dsn = """dbname='dronedb' user='postgres'
         host='localhost' password='postgres'"""
connection = dbapi2.connect(dsn)
cursor = connection.cursor()
statement = "SELECT * FROM CUSTOMER WHERE username=%s;"
cursor.execute(statement,('bilginmu166',))
password = cursor.fetchone()
cursor.close()

