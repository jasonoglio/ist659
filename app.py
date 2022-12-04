

from flask import Flask, render_template, request, make_response, Response, session
from sqlalchemy import create_engine
from sqlalchemy.orm import close_all_sessions
from mysql import connector
import mysql.connector as sqlcon  # must use as because other package also has .connect

import pandas as pd
from datetime import datetime
from datetime import timedelta
import numpy as np
import time
from flask_mysqldb import MySQL, MySQLdb
import MySQLdb.cursors
import connectorx as cx

from forms import LoginForm





app = Flask(__name__)
app.secret_key = "wierugbnqierniqenrgpiquenrgpiquerngpqieurng"

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=10)
app.config["SESSIOn_REFRESH_EACH_REQUEST"] =  True

mysql = MySQL(app)

@app.route('/nav')
def nav():
    return render_template("nav.html")

@app.route('/', methods=["GET", "POST"])
def index():
    form = LoginForm()

    conn = f'mysql://admin:istIST659@ist659-db.cqx6ke9fapft.us-east-1.rds.amazonaws.com:3306/ist659'  # connection token
    query = 'SELECT * FROM ist659.fake_table'  # query string
    data = cx.read_sql(conn, query, return_type='pandas')
    print(data.head(5))

    return render_template("index.html", form=form, data=data.to_dict(orient='records'))

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        print('test')
        form_data = request.form
        print(form_data.get('email'))
        print(form_data.get('password'))
        session['customer'] = form_data.get('email')

        conn = f'mysql://admin:istIST659@ist659-db.cqx6ke9fapft.us-east-1.rds.amazonaws.com:3306/ist659'  # connection token
        query = 'SELECT * FROM ist659.fake_table'  # query string
        data = cx.read_sql(conn, query, return_type='pandas')
        print(data.head(5))

        conn = f'mysql://admin:istIST659@ist659-db.cqx6ke9fapft.us-east-1.rds.amazonaws.com:3306/ist659'  # connection token
        query = 'SELECT customer_email FROM ist659.customers'  # query string
        customer_email_list = cx.read_sql(conn, query, return_type='pandas')
        customer_email_list = customer_email_list['customer_email'].to_list()
        print(customer_email_list)

        engine = create_engine('mysql://admin:istIST659@ist659-db.cqx6ke9fapft.us-east-1.rds.amazonaws.com:3306/ist659')

        if form_data.get('email') in customer_email_list:
            pass
        else:
            update_sql = '''
            INSERT INTO `ist659`.`customers` (`customer_email`, `customer_password`) VALUES ('%s', '%s');
            '''%(form_data.get('email'), form_data.get('password'))
            engine.execute(update_sql)


        return render_template("main.html", data=data.to_dict(orient='records'))




if __name__ == "__main__":
    app.run(host="0.0.0.0")
    app.run(debug=True)

