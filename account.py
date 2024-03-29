from flask import Flask, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

DEBUG=os.getenv("DEBUG")
PORT=os.getenv("NODE_PORT")
 
# Google Cloud SQL CONFIG
PASSWORD = os.getenv("PASSWORD")
PUBLIC_IP_ADDRESS = os.getenv("PUBLIC_IP_ADDRESS")
DBNAME = os.getenv("DBNAME")
PROJECT_ID = os.getenv("PROJECT_ID")
INSTANCE_NAME = os.getenv("INSTANCE_NAME")
 
# Configuration - Hardcoded credentials so Docker image will run properly
app.config["SECRET_KEY"] = "yoursecretkey"
app.config["SQLALCHEMY_DATABASE_URI"]= f"mysql+mysqldb://root:wherebnb@34.173.224.187/accounts?unix_socket=/cloudsql/useful-memory-414316:wherebnb-dev-db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= True

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
    userType = db.Column(db.Integer, nullable = False)          # 1 = Guest, 2 = Owner

@app.route('/add', methods =['POST'])
def add():
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

@app.route('/view_all')
def view_all():
    # fetches all the accounts
    accounts = Accounts.query.all()

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
        'data': response
    }, 200)

@app.route('/view/<id>')
def view(id):
    account = Accounts.query.filter_by(id = id).first()

    if not account:
        responseObject = {
                'status' : 'fail',
                'message': 'User not found!'
            }
        return make_response(responseObject, 400)
        
    response = {
        "id" : account.id,
        "username" : account.username,
        "firstName" : account.firstName,
        "lastName" : account.lastName,
        "email" : account.email,
        "password" : account.password,
        "userType" : account.userType
    }
 
    return make_response({
        'status' : 'success',
        'data': response
    }, 200)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=PORT, debug=DEBUG)

# docker build -t damonwong2022148/account:1.0 ./
# docker run -p 5000:5000 -e dbURL=mysql+mysqldb://root:wherebnb@34.173.224.187/accounts?unix_socket=/cloudsql/useful-memory-414316:wherebnb-dev-db damonwong2022148/account:1.0