#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, request
app = Flask(__name__, static_url_path="")

import MySQLdb as mdb
from datetime import datetime,timedelta
import dateutil.parser

import ConfigParser

import json
import pdb
@app.route("/")
def defaultPath():
    return app.send_static_file("index.html")

    
def get_mysql_params():
    config = ConfigParser.ConfigParser()

    with app.open_resource('config.ini') as f:
        config.readfp(f)

        mysql_host = config.get("mysql", "host")
        mysql_user = config.get("mysql", "user")
        mysql_passwd = config.get("mysql", "password")
        mysql_db = config.get("mysql", "db")

    return mysql_host, mysql_user, mysql_passwd, mysql_db


# Paramaters:
# since         ISO timestamp of where to start samples from
# maxPoints     maximum number of samples returned
@app.route("/getData")
def getData():
    mysql_host, mysql_user, mysql_passwd, mysql_db = get_mysql_params()


    # if not specified, 1000 points outght to be enough
    maxPoints = request.args.get("maxPoints", default=1000, type=int)
        
    if request.args.get("since") is None:
        limitDate = datetime.now() - timedelta(days=1)
    else:
        limitDate = dateutil.parser.parse( request.args.get("since") )
        
    # Count how many datapoints are available between 'since' and now
    try:
        conn = mdb.connect(mysql_host, mysql_user, mysql_passwd, mysql_db)
        cur = conn.cursor(mdb.cursors.DictCursor)
        cur.execute("SELECT COUNT(*) AS count FROM fridge WHERE time > %s", (limitDate,))
        recordset = cur.fetchall()      
    except mdb.Error, e:
        return ""
    finally:
        if conn:
            conn.close()
         
    # Calculate the divisor we need for selecting no more than maxPoints samples
    row = recordset[0]
    numSamples = row["count"]
    modulus = int(numSamples / maxPoints)
     
    conn = mdb.connect(mysql_host, mysql_user, mysql_passwd, mysql_db)
  
    try:
        cur = conn.cursor(mdb.cursors.DictCursor)
        cur.execute("SELECT * FROM fridge WHERE time > %s AND ID mod %s=0 ORDER BY time DESC", (limitDate,str(modulus)))
        recordset = cur.fetchall()        
        
    except mdb.Error, e:
        return ""
    finally:
        conn.close()
            
    datasetArray = [{"name": "Temperature", "data": []}, {"name": "Battery Voltage", "data": []}]
    epoch = datetime.utcfromtimestamp(0)
    
    for row in recordset:
        time = (row['time'] - epoch).total_seconds()
        temperature = row['temperature']
        batteryVoltage = row['batteryVoltage']
        datasetArray[0]["data"].insert(0, {"x": time, "y": temperature} )
        datasetArray[1]["data"].insert(0, {"x": time, "y": batteryVoltage} )
        
    return json.dumps(datasetArray)

    
    
@app.route("/last24hours")
def getLast24HourData():

    mysql_host, mysql_user, mysql_passwd, mysql_db = get_mysql_params()
    
    conn = mdb.connect(mysql_host, mysql_user, mysql_passwd, mysql_db)

    try:
        limitDate = datetime.now() - timedelta(days=1)
        cur = conn.cursor(mdb.cursors.DictCursor)
        cur.execute("SELECT * FROM fridge WHERE time > %s AND ID mod 10=0 ORDER BY time DESC", (limitDate,))
        recordset = cur.fetchall()        
        
    except mdb.Error, e:
        return ""
    finally:
        conn.close()

    datasetArray = [{"name": "Temperature", "data": []}, {"name": "Battery Voltage", "data": []}]
    epoch = datetime.utcfromtimestamp(0)
    
    for row in recordset:
        time = (row['time'] - epoch).total_seconds()
        temperature = row['temperature']
        batteryVoltage = row['batteryVoltage']
        datasetArray[0]["data"].insert(0, {"x": time, "y": temperature} )
        datasetArray[1]["data"].insert(0, {"x": time, "y": batteryVoltage} )
        
    return json.dumps(datasetArray)
    
if __name__ == "__main__":
    app.run(debug=True)
    
