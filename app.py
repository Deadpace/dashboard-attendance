from flask import Flask, render_template, request, flash, redirect, url_for
import os
import pandas as pd

app = Flask(__name__)
app.secret_key = "secret!"
data = [file.split('.')[0] for file in os.listdir("data")]
dates = [file.split('_')[1] for file in data]


@app.route('/')
def index():
    return render_template('index.html',dates = enumerate(zip(dates,data)))

@app.route('/employee/<string:file_name>')
def employee(file_name):
    file = pd.read_csv(f"data//{file_name}.csv",usecols =['Name','Time','Check Out Time']).to_dict(orient="index")
    return render_template('employee.html',file= file)

@app.route('/add_employee')
def add_employee():
    return render_template("add-employee.html")

@app.route('/add_into_data',methods=["POST"])
def add_into_data():
    if request.form:
        data = request.form
        print(data)
        flash("Employee Added")
        return redirect(url_for("add_employee"))

if __name__== "__main__":
    app.run(debug=True)