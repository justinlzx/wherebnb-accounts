from flask import Flask, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
 
app = Flask(__name__)
 
# Google Cloud SQL (to be stored in .env file later)
PASSWORD ="wherebnb"
PUBLIC_IP_ADDRESS ="34.173.224.187"
DBNAME ="account"
PROJECT_ID ="useful-memory-414316"
INSTANCE_NAME ="wherebnb-dev-db"
 
# Configuration
app.config["SECRET_KEY"] = "yoursecretkey"
app.config["SQLALCHEMY_DATABASE_URI"]= f"mysql+mysqldb://root:{PASSWORD}@{PUBLIC_IP_ADDRESS}/{DBNAME}?unix_socket=/cloudsql/{PROJECT_ID}:{INSTANCE_NAME}"
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
    loyaltyPoints = db.Column(db.Integer, nullable = False)
    # to be hashed later
    password = db.Column(db.String(255), nullable = False)

# To test/add functionality later
@app.route('/add', methods =['POST'])
def add():
    # getting name and email
    id = request.form.get('id')
    username = request.form.get('username')
    firstName = request.form.get('firstName')
    lastName = request.form.get('lastName')
    email = request.form.get('email')
    loyaltyPoints = request.form.get('loyaltyPoints')
    password = request.form.get('password')

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
                loyaltyPoints = loyaltyPoints,
                password = password
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
    """
    if (db.session.scalars(
      db.select(Accounts).filter_by(id=id).
      limit(1)
      ).first()
      ):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "id": id
                },
                "message": "Account already exists."
            }
        ), 400

    data = request.get_json()
    account = Accounts(id, **data)
        "id": 1,
        "username": "Alpha",
        "firstName": "Testing",
        "lastName": "OneTwoThree",
        "email": "betacharlie@delta.com",
        "loyaltyPoints": 0,
        "password": "wordpass"
    try:
        db.session.add(account)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "id": id
                },
                "message": "An error occurred creating the account."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": account.json()
        }
    ), 201
    """

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
            "loyaltyPoints" : account.loyaltyPoints,
            "password" : account.password
        })
 
    return make_response({
        'status' : 'success',
        'message': response
    }, 200)
 

if __name__ == "__main__":
    # serving the app directly
    app.run()