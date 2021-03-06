#from crypt import methods
from flask_login import current_user, login_user
#from requests import request
from animal_shelter import app, db
from animal_shelter.models import Breed_description, Adopter, Animal, Application
from animal_shelter.models import insert_user, get_all_animals, get_single_pet_info
from animal_shelter.models import search_user_by_id, get_apply, apply_new, get_all_applications
from animal_shelter.models import delete_animal_by_id, delete_apply_by_id,get_submitted_apply
from animal_shelter.models import get_apply_by_apply_id, approve_apply, change_password
from animal_shelter.models import decline_apply,  search_animals, search_animal_by_name, add_animal
from flask import render_template
from flask import request, flash, redirect, url_for
from flask_login import login_required, logout_user
from datetime import date 
#from flask_restful import reqparse
from sqlalchemy import or_ , text
from werkzeug.security import generate_password_hash, check_password_hash

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
            user = Adopter.query.filter(Adopter.username==username).first()
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
        mobile = request.form['mobile']
        gender = request.form['gender']
        post = request.form['post']
        occupation = request.form['occupation']
        age = request.form['age']

        if not username or not password or not user_type:
            flash('Invalid input.')
            return redirect(url_for('signup'))
        
        #test_user = User.query.filter(User.username == username).all()
        sql = """
        SELECT *
        FROM adopter
        WHERE username= :var
        """
        test_user = db.engine.execute(text(sql),{'var':username}).fetchone()

        if test_user:
            flash("Username already exists, try another one.")
            return redirect( url_for('signup') )

        typ = True if user_type == 'shelter' else False
        gen = True if gender == 'male' else False

        insert_user(username, password, typ, mobile, gen, age, occupation, post)

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
        #animals = Animal.query.filter().all()
        animals = get_all_animals()
        return render_template('shelter_home.html', animals=animals)
    else:
        #animals = Animal.query.filter().all()
        animals = get_all_animals()
        return render_template('user_home.html', animals=animals)

@app.route('/single_pet/<int:animal_id>')
@login_required
def single_pet(animal_id):
    """show the page of a certain pet."""
    #animal_a= Animal.query.filter(Animal.id==animal_id).first()
    animal, breed_info= get_single_pet_info(animal_id)
    #return (animal_info[1])
    return render_template('animal_detail.html', animals=animal, 
        descriptions=breed_info)

@app.route('/single_user/<int:user_id>')
@login_required
def single_user(user_id):
    """show the page of a certain user."""
    #user_a= User.query.filter(User.id==user_id).first()
    user_a = search_user_by_id(user_id)
    return render_template('user_detail.html', users=user_a)


@app.route('/apply/<int:animal_id>/<int:user_id>') 
@login_required
def apply(animal_id,user_id):
    '''add this application into database'''
    #apply = Application.query.filter(Application.user_id==current_user.id, Application.#animal_id==animal_id).first()
    apply = get_apply(user_id, animal_id)
    if apply:
        flash("You have already applied for this pet.")
        #animals = Animal.query.filter().limit(6)
        animals = get_all_animals()
        return render_template('user_home.html', animals=animals)
    else:
        '''application = Application(animal_id=animal_id, user_id=user_id, 
        date=date.today().strftime("%x"), state="submitted")
        db.session.add(application)
        db.session.commit()'''
        apply_new(animal_id, user_id)

    '''return to the user home page'''
    flash("Application submitted.")
    #animals = Animal.query.filter().limit(6)
    animals = get_all_animals()
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
    #applications = db.session.query(Application).filter(Application.user_id == current_user.id).all()
    applications = get_all_applications()
    if not applications:
        flash("You have not made any application yet")
    return render_template('user_application.html', applications=applications)

@app.route('/shelter_delete/<int:animal_id>')
@login_required
def shelter_delete(animal_id):
    '''For shelter delete certain animal from the database'''
    '''animal = Animal.query.get_or_404(animal_id)
    db.session.delete(animal)
    db.session.commit()'''
    delete_animal_by_id(animal_id)
    delete_apply_by_id(animal_id)
    '''applications = Application.query.filter(Application.animal_id==animal_id).all()
    for application in applications:
        db.session.delete(application)
    db.session.commit()'''

    #animals = Animal.query.filter().limit(6)
    animals = get_all_animals()
    return render_template('shelter_home.html',animals=animals)

@app.route('/shelter_application')
@login_required
def shelter_application():
    #applications = Application.query.filter(Application.state == "submitted").all()
    #animals = Animal.query.filter(Animal.id == Application.animal_id ).all()
    applications = get_submitted_apply()
    return render_template('shelter_application.html',applications=applications)

@app.route('/edit/<int:application_id>', methods=['GET','POST'])
@login_required
def edit(application_id):
    if request.method == 'POST':
        #application = Application.query.get_or_404(application_id)
        application = get_apply_by_apply_id(application_id)
        decision = request.form['decision']
        if decision == 'Approve':
            #application.state = 'Approved'
            approve_apply(application_id)
            flash('Approved application: ' + str(application_id))
        else:
            #application.state = 'Declined'
            decline_apply(application_id)
            flash('Declined application: ' + str(application_id))
        #db.session.commit()
        return redirect( url_for('shelter_application') )

    return render_template('edit.html')

@app.route('/search', methods=['GET','POST'])
@login_required
def search():
    if request.method == 'POST':
        cat_or_not = request.form['cat']=='True'
        desex_or_not= request.form['desexed']=='True'
        breed = request.form['breed']
        b1=breed[1:2].lower()
        b2=breed[-3:-2].lower()

        color = request.form['color']
        #weight = request.form['weight']
        '''animals = Animal.query.filter(Animal.color==color, 
                Animal.cat==cat_or_not, Animal.desexed==desex_or_not).filter(
            or_(Animal.breed.like("%" + b1 + "%") if breed is not None else ""),
            (Animal.breed.like("%" + b2 + "%") if breed is not None else "")
        ).all()'''
        animals = search_animals(color, cat_or_not, desex_or_not, breed)
         
        #if len(animals)==0:
        if not animals:
            flash("No such animals can satisfy your desire. Try some other requirements.")          
            return render_template('search.html')
   
        #if not current_user.is_authenticated: 
        if current_user.type == True:
           return render_template('shelter_home.html',animals=animals)
        else:
           return render_template('user_home.html', animals=animals)
        
    else:
        return render_template('search.html')

@app.route('/add',methods=['GET','POST'])
@login_required
def add():
    if current_user.type == False:
        flash("You don't have the right to add animals.")
        return redirect( url_for('home') )

    if request.method == 'POST':
        cat = request.form['cat']=='true'
        name = request.form['animal_name']
        desexed = request.form['desexed']=='true'
        breed = request.form['breed']
        color = request.form['color']
        weight = request.form['weight']
        disease = request.form['disease']
        picture = request.form['picture']

        #test_animal = Animal.query.filter(Animal.name == name).all()
        test_animal = search_animal_by_name(name)
        if test_animal:
            flash('Animal name already existed, try another one.')
            return redirect( url_for('add') )

        '''animal = Animal(name=name, cat=cat, desexed=desexed, breed=breed, color=color, weight=weight, disease=disease, picture=picture)
        db.session.add(animal)
        flash("Now added successfully! ")

        db.session.commit()'''
        add_animal(name=name, cat=cat, desexed=desexed, breed=breed, color=color, weight=weight, disease=disease, picture=picture)
        return redirect( url_for('home') )

    else:
        return render_template('add.html')




@app.route('/usersetting',methods=['GET', 'POST'])
@login_required
def usersetting():
    if request.method == 'POST':
        #get the list data
        username = request.form['username']
        o_pass = request.form['o_pass']
        n_pass = request.form['n_pass']
        c_pass = request.form['c_pass']
        n_hash = generate_password_hash(n_pass)
     
        if not current_user.username==username:
            flash('Invalid username, check it')
            return redirect(url_for('usersetting'))
        
        if not check_password_hash(current_user.password_hash, o_pass):
            flash('Invalid old password')
            return redirect(url_for('usersetting'))
          
        if check_password_hash(current_user.password_hash, n_pass):
            flash('Same password, try a new one')
            return redirect(url_for('usersetting'))

        if not check_password_hash(n_hash, c_pass): 
            flash('The two new passwords do not match, entry again')
            return redirect(url_for('usersetting')) 

        '''current_user.password_hash = n_hash
        flash('Password reset successfully')
        db.session.commit()'''
        change_password(current_user.id, n_hash)

        return redirect({{ url_for('home') }})
       

        #return redirect(url_for('home'))
    else:
        return render_template('user_setting.html')
        

            

