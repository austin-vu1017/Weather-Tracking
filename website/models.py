# create database model

# import db = SQLAlchemy() FROM __init__.py. flask_login assists in users logging in and user objects inherit from UserMixin
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))

    # date is created displaying when note was made. Date info is properly added using func module
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    # stores the user's ID that created the note. References the user's ID from another table. Foreign key forces user_id to hold user.id value.
    # Note: Foreign key references the object in lower case name
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    # ID is primary key. unique to each user and should have no duplicates
    id = db.Column(db.Integer, primary_key=True)

    # unique email. no duplicate email address in database
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    # everytime a note is created, add into this user's note relationship that note ID.
    # Note: .relationship has to reference the EXACT name of the class
    notes = db.relationship('Note')