from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@34.173.224.187:3306/accounts'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Account(db.Model):
    __tablename__ = 'account'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    firstName = db.Column(db.String(20), nullable=False)
    lastName = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    loyaltyPoints = db.Column(db.Integer, nullable=False)

    def __init__(self, id, username, firstName, lastName, email, password, loyaltyPoints):
        self.id = id
        self.username = username
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = password
        self.loyaltyPoints = loyaltyPoints

    def json(self):
        return {"id": self.id, "username": self.username, "firstName": self.firstName, "lastName": self.lastName,
                "email": self.email, "password": self.password, "loyaltyPoints": self.loyaltyPoints}



@app.route("/account")
def get_all():
    accountlist = db.session.scalars(db.select(Account)).all()

    if len(accountlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "accounts": [account.json() for account in accountlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no accounts."
        }
    ), 404


@app.route("/account/<string:isbn13>")
def find_by_isbn13(isbn13):
    account = db.session.scalars(
        db.select(Account).filter_by(isbn13=isbn13).
        limit(1)
).first()

    if account:
        return jsonify(
            {
                "code": 200,
                "data": account.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Account not found."
        }
    ), 404

@app.route("/account/<string:isbn13>", methods=['POST'])
def create_account(isbn13):
    if (db.session.scalars(
        db.select(Account).filter_by(isbn13=isbn13).
        limit(1)
).first()
):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "isbn13": isbn13
                },
                "message": "Account already exists."
            }
        ), 400

    data = request.get_json()
    account = Account(isbn13, **data)


    try:
        db.session.add(account)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "isbn13": isbn13
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

if __name__ == '__main__':
    app.run(port=5000, debug=True)
