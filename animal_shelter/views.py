from crypt import methods
import re
from flask_login import login_user
from requests import request
from animal_shelter import app, db
from animal_shelter.models import User, Animal, Application
from flask import render_template
from flask import request, flash, redirect, url_for

@app.route('/')
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))
        
        else:
            user = User.query.filter(User.username==username).first()
            if user:
                # there is such a user
                if user.validate_password(password):
                    return redirect(url_for('home'))
                else:
                    # wrong password
                    flash('Wrong password.')
                    return redirect(url_for('login'))
            else:
                # no such user
                flash('No such a user. Please signup first.')
                return redirect(url_for('login'))
    else:
        # GET method
        return render_template('login.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('signup'))

        user = User(username=username)
        user.set_password(password=password)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login'))

    else:
        return render_template('signup.html')