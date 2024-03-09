from flask import Flask, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from os import environ

load_dotenv()
app = Flask(__name__)
 
# Google Cloud SQL CONFIG
PASSWORD = os.getenv("PASSWORD")
PUBLIC_IP_ADDRESS = os.getenv("PUBLIC_IP_ADDRESS")
DBNAME = os.getenv("DBNAME")
PROJECT_ID = os.getenv("PROJECT_ID")
INSTANCE_NAME = os.getenv("INSTANCE_NAME")
 
# Configuration
app.config["SECRET_KEY"] = "yoursecretkey"
app.config["SQLALCHEMY_DATABASE_URI"]= f"mysql+mysqldb://root:{PASSWORD}@{PUBLIC_IP_ADDRESS}/{DBNAME}?unix_socket=/cloudsql/{PROJECT_ID}:{INSTANCE_NAME}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= False

app.app_context().push()

db = SQLAlchemy(app)

# Account ORM for SQLAlchemy
class Accounts(db.Model):
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    username = db.Column(db.String(20), nullable = False)
    firstName = db.Column(db.String(20), nullable = False)
    lastName = db.Column(db.String(20), nullable = False)
    email = db.Column(db.String(255), nullable = False, unique = True)
    password = db.Column(db.String(255), nullable = False)      # to be hashed later
    userType = db.Column(db.Integer, nullable = False)

# To test/add functionality later
@app.route('/add', methods =['POST'])
def add():
    # getting name and email
    id = request.form.get('id')
    username = request.form.get('username')
    firstName = request.form.get('firstName')
    lastName = request.form.get('lastName')
    email = request.form.get('email')
    password = request.form.get('password')
    userType = request.form.get('userType')

    # checking if account already exists
    account = Accounts.query.filter_by(id = id).first()
    if not account:
        try:
            # creating Accounts object
            account = Accounts(
                id = id,
                username = username,
                firstName = firstName,
                lastName = lastName,
                email = email,
                password = password,
                userType = userType
            )

            # adding the fields to accounts table
            db.session.add(account)
            db.session.commit()

            # response
            responseObject = {
                'status' : 'success',
                'message': 'Successfully registered.'
            }
 
            return make_response(responseObject, 200)

        except:
            responseObject = {
                'status' : 'fail',
                'message': 'Some error occurred !!'
            }
 
            return make_response(responseObject, 400)

    else:
        # if user already exists then send status as fail
        responseObject = {
            'status' : 'fail',
            'message': 'User already exists !!'
        }
 
        return make_response(responseObject, 403)

@app.route('/view')
def view():
    # fetches all the accounts
    accounts = Accounts.query.all()
    # response list consisting user details
    response = list()
    for account in accounts:
        response.append({
            "id" : account.id,
            "username" : account.username,
            "firstName" : account.firstName,
            "lastName" : account.lastName,
            "email" : account.email,
            "password" : account.password,
            "userType" : account.userType
        })
 
    return make_response({
        'status' : 'success',
        'message': response
    }, 200)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)