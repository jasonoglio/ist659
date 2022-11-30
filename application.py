

from flask import Flask, render_template, request, make_response, Response, session
from sqlalchemy import create_engine
from sqlalchemy.orm import close_all_sessions
from mysql import connector
import mysql.connector as sqlcon  # must use as because other package also has .connect
import pyodbc as pyodbc
import pandas as pd
from datetime import datetime
from datetime import timedelta
import numpy as np
import time
from flask_mysqldb import MySQL, MySQLdb
import MySQLdb.cursors
import connectorx as cx


application = Flask(__name__)
application.secret_key = "wierugbnqierniqenrgpiquenrgpiquerngpqieurng"

mysql = MySQL(application)

@application.route('/nav')
def nav():
    return render_template("nav.html")

@application.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'GET':

        conn = f'mysql://admin:istIST659@ist659-db.cqx6ke9fapft.us-east-1.rds.amazonaws.com:3306/ist659'  # connection token
        query = 'SELECT * FROM ist659.fake_table'  # query string
        # https://github.com/sfu-db/connector-x
        data = cx.read_sql(conn, query, return_type='pandas')
        print(data.head(5))
        # connectorX is faster but something is wrong with the df

        return render_template("index.html", data=data.to_dict(orient='records'))


if __name__ == "__main__":
    application.run(host="0.0.0.0")
    application.run(debug=True)

