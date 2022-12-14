

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
from forms import SearchForm





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
    form = LoginForm('/')

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

            pw_query = '''
                    SELECT customer_password FROM ist659.customers WHERE customer_email IN ('%s')
                    '''%(form_data.get('email'))

            customer_password = cx.read_sql(conn, pw_query, return_type='pandas')
            customer_password = customer_password['customer_password'].to_list()
            print(customer_password)

            if form_data.get('password') in customer_password:
                form = SearchForm('login')
                return render_template("main.html", form=form, data=data.to_dict(orient='records'))
            else:
                form = LoginForm('/')
                return render_template("index.html", form=form)

        else:
            update_sql = '''
            INSERT INTO `ist659`.`customers` (`customer_email`, `customer_password`, `customer_firstname`, 
            `customer_lastname`, `customer_phone`) VALUES ('%s', '%s', '%s', '%s', '%s');
            '''%(form_data.get('email'), form_data.get('password'), form_data.get('first_name'), form_data.get('last_name'),
                 form_data.get('phone'))
            engine.execute(update_sql)

        return render_template("main.html", data=data.to_dict(orient='records'))

@app.route('/search', methods=["GET", "POST"])
def search():
    if request.method == 'POST':
        print('test')
        form_data = request.form
        print(form_data.get('search'))

        # this route has to return a dataframe

        data = [[1, 'tour', 'venue', 'opener', 'headliner', 'event_date', 'doors_open']]
        df = pd.DataFrame(data, columns=['event_id', 'tour', 'venue', 'opener', 'headliner', 'event_date', 'doors_open'])
        # make a test dataframe
        print(df)

        event_id = list(df['event_id'])
        tour = list(df['tour'])
        venue = list(df['venue'])
        opener = list(df['opener'])
        headliner = list(df['headliner'])
        event_date = list(df['event_date'])
        doors_open = list(df['doors_open'])

        dict_list = [{'event_id': event_id[i], 'tour': tour[i], 'venue': venue[i],
                      'opener': opener[i], 'headliner': headliner[i], 'event_date': event_date[i],
                      'doors_open': doors_open[i]} for i in range(len(event_id))]

        return render_template("search.html", dict_list=dict_list)


@app.route('/buy', methods=["GET", "POST"])
def buy():
    if "buy" in request.form:
        print(request.form['buy'])
        buy = int(request.form['buy'])

        return render_template("buy.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0")
    app.run(debug=True)

