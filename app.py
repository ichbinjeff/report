from flask import Flask
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

@app.route('/db')
def db():
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cur = conn.cursor()
    cur.execute('''SELECT * FROM COMPANY;''')
    rows = cur.fetchall()
    rst = ""
    for row in rows:
        rst += "ID = ", row[0]
        rst += "NAME = ", row[1]
        rst += "ADDRESS = ", row[2]
        rst += "SALARY = ", row[3], "\n"
    print "Operation done successfully"

    conn.commit()
    conn.close()
    return rst

