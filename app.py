from flask import Flask, render_template, request, flash, redirect, url_for
import os
import json
import pymongo
import pandas as pd

app = Flask(__name__)
app.secret_key = "secret!"


#loading config.json file for configurations
with open('config.json') as f:
    config = json.load(f)

mongodb_url = config["mongodb_url"]
database_name = config["database_name"]
client = pymongo.MongoClient(mongodb_url)
DBlist = client.list_database_names()
if database_name in DBlist:
    print(f"DB: '{database_name}' exists")
else:
    print(f"DB: '{database_name}' not yet present OR no collection is present in the DB")

database = client[database_name]
 

@app.route('/')
def index():
    data = sorted(database.list_collection_names(),reverse=True)
    dates = [file.split('_')[1] for file in data]
    return render_template('index.html',dates = enumerate(zip(dates,data)))

@app.route('/employee/<string:file_name>')
def employee(file_name):
    collection = database[file_name]
    file = [i for i in collection.find()]
    return render_template('employee.html',file= file)

@app.route('/add_employee')
def add_employee():
    return render_template("add-employee.html", style = "display: none")

@app.route('/add_into_data',methods=["POST"])
def add_into_data():
    if request.method == "POST":
        if request.form:
            data = request.form
            print(data)
            # flash("Employee Added")
            return render_template("add-employee.html", style = "")

if __name__== "__main__":
    app.run(debug=True)