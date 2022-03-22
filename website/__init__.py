from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# create database
db = SQLAlchemy()
DB_NAME = 'database.db'

# initializes app
def create_app():
    # __name__ represents name of file and intiliazes Flask
    app = Flask(__name__)

    # token key of the site. In work setting, NEVER SHARE THIS. 
    app.config['SECRET_KEY'] = 'qazwsxedcrfvtgbyhnujmikolp'

    # SQLAlchemy database is stored/located at this location
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    # take the database defined and use it along with the Flask app
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note
    create_database(app)
    
    # initiates login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # load the user by searching for the user's primary key ID
    @login_manager.user_loader
    def load_user(id): return User.query.get(int(id))

    return app

def create_database(app):
    # if database does not exist in this folder, create database
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')