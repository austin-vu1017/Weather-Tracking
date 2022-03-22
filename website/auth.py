# anything involving logging in the website goes here

# import render_template to show content of the page, request to get information, flash to display messages, and werkzeug.security to encrypt password
from flask import Blueprint as bp, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

# define authentication file as blueprint
auth = bp('auth', __name__)

# methods will allow login and signup to accept GET and POST requests
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # request info inputted by user and store it to variables.
        email = request.form.get('email')
        password = request.form.get('password')

        # filters the database for users' with matching email
        user = User.query.filter_by(email=email).first()
        if user:
            # compared the hash version of the inputted password from user to hashed password in the currently selected user
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')

                # logging in with this user and remember that the user is logged in until user clears history/session or web server restarts
                login_user(user, remember=True)
                
                # redirect user to the home page referenced in views.py
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template('login.html', user=current_user)

# login_required will determine if user can view the page. this applies ONLY IF user is logged in
@auth.route('/logout')
@login_required
def logout():
    logout_user()

    # redirects logged out user to the login page
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        # backend will receive the information inputted by user
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        uncom_pw = request.form.get('unconfirmed_pw')
        com_pw = request.form.get('confirmed_pw')
        
        # information will be checked if valid and not already existing in database.
        user = User.query.filter_by(email=email).first()
        if user: 
            flash('Email already exists.', category='error')
        elif len(email) < 4: 
            flash('Email must be great than 3 characters.', category='error')
        elif len(first_name) < 2: 
            flash('First name must be greater than 1 characters.', category='error')
        elif uncom_pw != com_pw: 
            flash("Passwords don't match.", category='error')
        elif len(uncom_pw) < 7: 
            flash('Password must be at least 7 characters.', category='error')
        else:
            # new_user object will hold the new sign-up info. password will go through hash function. however, password can't be 'unhashed'
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(com_pw, method='sha256')) 

            # add new_user to database
            db.session.add(new_user)

            # update the database
            db.session.commit()
            login_user(user, remember=True)
            flash('Account created!', category='success')

            return redirect(url_for('views.home'))

    return render_template('sign_up.html', user=current_user)