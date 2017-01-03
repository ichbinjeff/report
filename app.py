from flask import Flask
from flask import render_template
from flask import request

import os
import psycopg2
import urlparse

app = Flask(__name__)

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello():
    return 'Hello, World'

@app.route('/createTable')
def createTable():
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cur = conn.cursor()
    cur.execute('''DROP TABLE IF EXISTS COMPANY; CREATE TABLE COMPANY
           (ID INT PRIMARY KEY     NOT NULL,
           NAME           TEXT    NOT NULL,
           AGE            INT     NOT NULL,
           ADDRESS        CHAR(50),
           SALARY         REAL);''')
    print "Table created successfully"

    conn.commit()
    conn.close()
    return 'everything is good'

@app.route('/insert')
def insert():
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cur = conn.cursor()
    cur.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
          VALUES (1, 'Paul', 32, 'California', 20000.00 )");

    cur.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
          VALUES (2, 'Allen', 25, 'Texas', 15000.00 )");

    cur.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
          VALUES (3, 'Teddy', 23, 'Norway', 20000.00 )");

    cur.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
          VALUES (4, 'Mark', 25, 'Rich-Mond ', 65000.00 )");

    conn.commit()
    print "Records created successfully"
    conn.close()
    return 'inserted data into db'


@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/select')
def select():
    name = request.args.get('name')
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cur = conn.cursor()
    sql = 'SELECT id, name, address, salary FROM COMPANY WHERE NAME=' + '\'' + name + '\'' + ';'
    cur.execute(sql)
    rows = cur.fetchall()
    rst = "rst"
    for row in rows:
        rst += "ID = " + str(row[0]) + "\n"
        rst += "NAME = " + str(row[1]) + "\n"
        rst += "ADDRESS = " + str(row[2])+ "\n"
        rst += "SALARY = " + str(row[3]) + "\n"
    print "Operation done successfully"
    conn.close()
    return name + rst

