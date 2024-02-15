from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
# import uuid
from sqlalchemy import create_engine
from sqlalchemy import (
  Column,
  Computed,
  ForeignKey,
  Integer,
  MetaData,
  String,
  Table,
)

engine = create_engine(
    "spanner:///projects/useful-memory-414316/instances/wherebnb-dev-db/databases/account"
)

metadata = MetaData(bind=engine)

account = Table(
    "Account",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("firstName", String(20), nullable=False),
    Column("lastName", String(20), nullable=False),
    Column("email", String(255), nullable=False),
    Column("password", String(255), nullable=False),
    Column("loyaltyPoints", Integer, nullable=False),
)

metadata.create_all(engine)

account = Table("Account", MetaData(bind=engine), autoload=True)

with engine.begin() as connection:
  # id = uuid.uuid4().hex[:6].lower()           -Prevents creation of monotonically increasing primary keys; unneeded for our project for now
  connection.execute(account.insert(), {"id": 1, "firstName": "Bob", "lastName": "Allison", "email": "bob@allision.edu.sg", "password": "password1", "loyaltyPoints": 0})
