from flask import Flask, render_template, request, session, redirect, url_for
import json
import bcrypt
import pymongo
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "secret!"

#for setting the session time
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

#for reloading the templates
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

#loading config.json file for configurations
with open('config.json') as f:
    config = json.load(f)

#mongodb connection
mongodb_url = config["mongodb_url"]
client = pymongo.MongoClient(mongodb_url)

#attendance database
attendance_database = client[config["attendance_database_name"]]

#login database
login_collection_name = config[
    "login_collection_name"]  #collection name from config
login_database = client[config["login_database_name"]]
login_collection = login_database[login_collection_name]


@app.route('/')
def index():
    global login_collection
    login_collection = login_database[login_collection_name]
    if 'username' in session:
        return redirect(url_for('dashboard'))

    return render_template('login/login.html')


@app.route('/login', methods=['POST'])
def login():
    if request.method == "POST":
        if request.form:
            login_user = login_collection.find_one({'Email': request.form['email']})
            if login_user:
                if login_user["Role"] == 'Admin':
                    if bcrypt.checkpw(request.form['password'].encode('utf8'),
                                    login_user['Password']):
                        session['username'] = login_user['Name']
                        session['email'] = login_user['Email']
                        session.permanent = True
                        return redirect(url_for('index'))
                else:
                    return "Access Not Available!!"

            return 'Invalid username/password combination'
    else:
        return "Invalid Request"

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        data = sorted(attendance_database.list_collection_names(),
                      reverse=True)
        dates = [file.split('_')[1] for file in data]
        return render_template('dashboard/index.html',
                               dates=enumerate(zip(dates, data)))
    else:
        return redirect(url_for('index'))


@app.route('/employee/<string:collection_name>')
def employee(collection_name):
    if 'username' in session:
        collection = attendance_database[collection_name]
        content = [i for i in collection.find()]
        return render_template('dashboard/employee.html', content=content)
    else:
        return redirect(url_for('index'))


@app.route('/add_employee')
def add_employee():
    if 'username' in session:
        return render_template("dashboard/add-employee.html")
    else:
        return redirect(url_for('index'))


@app.route('/add_into_data', methods=["POST"])
def add_into_data():
    if request.method == "POST":
        if request.form:
            data = dict(request.form)
            global login_collection
            existing_user = login_collection.find_one(
                {'Email': request.form['Email']})

            if not existing_user:
                data['Password'] = bcrypt.hashpw(
                    data['Password'].encode('utf-8'), bcrypt.gensalt())
                login_collection.insert_one(data)
                login_collection = login_database[login_collection_name]
                return render_template("dashboard/add-employee.html",
                                       employee_add=True)

            return render_template("dashboard/add-employee.html",
                                   email_present=True)


@app.route('/change_password', methods=['POST'])
def change_password():
    if request.method == 'POST':
        if request.form:
            global login_collection
            user_details = login_collection.find_one(
                {'Email': session["email"]})
            if request.form["new_password"] == request.form["confirm_new_password"]:
                if bcrypt.checkpw(request.form['current_password'].encode('utf8'),
                        user_details['Password']):
                    new_password = bcrypt.hashpw(
                        request.form['new_password'].encode('utf-8'),
                        bcrypt.gensalt())
                    login_collection.update_one(
                        user_details, {"$set": {
                            "Password": new_password
                        }})
                    return redirect(url_for('logout'))
                else:
                    return "Current password does not match!!"
                
                
            else:
                return "New Password and Confirm New Password does not match"

    return redirect(url_for('dashboard'))


@app.route('/logout')
def logout():
    if 'username' in session:
        try:
            session.clear()
            return redirect(url_for('index'))
        except KeyError:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True, threaded=True)