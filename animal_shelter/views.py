from crypt import methods
from flask_login import current_user, login_user
from requests import request
from animal_shelter import app, db
from animal_shelter.models import User, Animal, Application
from flask import render_template
from flask import request, flash, redirect, url_for
from flask_login import login_required, logout_user
import time

@app.route('/')
def index():
    return render_template("index.html")


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
                    login_user(user)
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

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_type = request.form['type']

        if not username or not password or not user_type:
            flash('Invalid input.')
            return redirect(url_for('signup'))
        
        test_user = User.query.filter(User.name == username).all()
        if test_user:
            flash("Username already exists, try another one.")
            return redirect( url_for('signup') )

        if user_type == 'user':
            # normal user: type == False
            user = User(username=username,type=False)
        else:
            # shelter: type == Ture
            user = User(username=username,type=True)
        user.set_password(password=password)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login'))

    else:
        return render_template('signup.html')

@app.route('/logout')
@login_required 
def logout():
    logout_user() 
    flash('Goodbye.')
    return redirect(url_for('index')) 

@app.route('/home',methods=['GET','POST'])
@login_required
def home():
    if current_user.type == True:
        animals = Animal.query.filter().all()
        return render_template('shelter_home.html', animals=animals)
    else:
        animals = Animal.query.filter().all()
        return render_template('user_home.html', animals=animals)

@app.route('/signle_pet/<int:animal_id>')
@login_required
def single_pet(animal_id):
    """show the page of a certain pet."""
    return "certain page for animal " + str(animal_id)

@app.route('/apply/<int:animal_id>/<int:user_id>') 
@login_required
def apply(animal_id,user_id):
    '''add this application into database'''
    apply = Application.query.filter(Application.user_id==current_user.id, Application.animal_id==animal_id).first()
    if apply:
        flash("You have already apply for this pet.")
        animals = Animal.query.filter().limit(6)
        return render_template('user_home.html', animals=animals)

    application = Application(animal_id=animal_id, user_id=user_id, date='3/6/2022', state="submitted")
    db.session.add(application)
    db.session.commit()

    '''return to the user home page'''
    flash("Application submitted.")
    animals = Animal.query.filter().limit(6)
    return render_template('user_home.html', animals=animals)

@app.route('/application')
@login_required
def application():
    if current_user.type == True:
        return redirect(url_for('shelter_application'))
    else:
        return redirect(url_for('user_application'))

@app.route('/user_application')
@login_required
def user_application():
    '''This user's application'''
    applications = db.session.query(Application).filter(Application.user_id == current_user.id).all()
    return render_template('user_application.html', applications=applications)

@app.route('/shelter_delete/<int:animal_id>')
@login_required
def shelter_delete(animal_id):
    '''For shelter delete certain animal from the database'''
    animal = Animal.query.get_or_404(animal_id)
    db.session.delete(animal)
    db.session.commit()

    applications = Application.query.filter(Application.animal_id==animal_id).all()
    for application in applications:
        db.session.delete(application)
    db.session.commit() 

    animals = Animal.query.filter().limit(6)
    return render_template('shelter_home.html',animals=animals)

@app.route('/shelter_application')
@login_required
def shelter_application():
    applications = Application.query.filter(Application.state == "submitted").all()
    return render_template('shelter_application.html', applications=applications)

@app.route('/edit/<int:application_id>', methods=['GET','POST'])
@login_required
def edit(application_id):
    if request.method == 'POST':
        application = Application.query.get_or_404(application_id)
        decision = request.form['decision']
        if decision == 'Approve':
            application.state = 'Approved'
            flash('Approved application: ' + str(application_id))
        else:
            application.state = 'Declined'
            flash('Declined application: ' + str(application_id))
        db.session.commit()
        return redirect( url_for('shelter_application') )

    return render_template('edit.html')

@app.route('/search', methods=['GET','POST'])
@login_required
def search():
    if request.method == 'POST':
        return "This will return the search result using user_home or home.html"
    else:
        return "This is a demo search page. where you can submit your requiements"

@app.route('/add',methods=['GET','POST'])
@login_required
def add():
    if current_user.type == False:
        flash("You don't have the right to add animals.")
        return redirect( url_for('home') )

    if request.method == 'POST':
        cat = request.form['cat']
        name = request.form['animal_name']
        breed = request.form['breed']
        color = request.form['color']
        weight = request.form['weight']
        disease = request.form['disease']
        picture = request.form['picture']

        test_animal = Animal.query.filter(Animal.name == name).all()
        if test_animal:
            flash('Animal name already existed, try another one.')
            return redirect( url_for('add') )

        if cat == 'cat':
            animal = Animal(name=name, cat=True, breed=breed, color=color, weight=weight, disease=disease, picture=picture)
            db.session.add(animal)
            flash("add cat successfully ")
        else:
            animal = Animal(name=name, cat=False, breed=breed, color=color, weight=weight, disease=disease, picture=picture)
            db.session.add(animal)
            flash("add dog successfully ")

        db.session.commit()
        return redirect( url_for('home') )

    else:
        return render_template('add.html')
