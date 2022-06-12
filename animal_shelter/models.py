from animal_shelter import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy import text
from datetime import date

class Adopter(db.Model, UserMixin):  
    id = db.Column(db.Integer, primary_key=True)  
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    type = db.Column(db.Boolean)
    mobile = db.Column(db.String(30))
    gender = db.Column(db.Boolean) # kvinder 0 og mand 1
    age = db.Column(db.Integer)
    occupation = db.Column(db.String(20))
    post=db.Column(db.Integer)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

def set_password(password):
        return generate_password_hash(password)

def validate_password(password_hash, password):
        return check_password_hash(password_hash, password)

class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    cat = db.Column(db.Boolean) #True for cat, False for dog
    desexed = db.Column(db.Boolean)
    breed = db.Column(db.String(50))
    color = db.Column(db.String(20))
    weight = db.Column(db.Float())
    disease = db.Column(db.String(100))
    picture = db.Column(db.Text())
    
class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    animal_id = db.Column(db.Integer)
    date = db.Column(db.String(20))
    state = db.Column(db.String(50))

class Breed_description(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    breed = db.Column(db.String(50))
    details = db.Column(db.Text())

def insert_user(username, password, type, mobile, gender, age, occupation, post):
    id = len(db.engine.execute(text("select * from adopter")).fetchall()) + 1
    password_hash = set_password(password)
    insert_sql = """
        INSERT INTO adopter (id, username, password_hash, type, mobile, gender, age, occupation, post)
        VALUES (:id, :username, :password_hash, :type, :mobile, :gender, :age, :occupation, :post)
        """
    db.engine.execute(text(insert_sql).execution_options(autocommit=True),{'id': id, 'username':username, 'password_hash':password_hash,
                                        'type':type, 'mobile':mobile, 'gender':gender, 'age':age, 
                                        'occupation': occupation, 'post':post})

def get_all_animals():
    sql = """
        SELECT *
        FROM animal
    """
    animals = db.engine.execute(text(sql))
    return animals

def get_single_pet_info(animal_id):
    sql1 = """
        SELECT *
        FROM animal
        WHERE id = :id
    """
    sql2 = """
        SELECT *
        FROM breed_description
        WHERE breed = :b
    """

    animal = db.engine.execute(text(sql1),{'id': animal_id}).fetchone()
    breed = animal['breed']
    breed_info = db.engine.execute(text(sql2),{'b': breed}).fetchone()

    return animal, breed_info

def search_user_by_id(user_id):
    sql = """
        SELECT *
        FROM adopter
        WHERE id = :var
    """
    user = db.engine.execute(text(sql),{'var': user_id}).fetchone()
    return user

def get_apply(user_id, animal_id):
    sql = """
        SELECT *
        FROM application
        WHERE user_id = :x and animal_id = :y
    """
    apply = db.engine.execute(text(sql),{'x': user_id, 'y': animal_id}).fetchone()
    return apply

def get_apply_by_apply_id(application_id):
    sql = """
        SELECT *
        FROM application
        WHERE id = :x
    """
    apply = db.engine.execute(text(sql),{'x': application_id}).fetchone()
    return apply

def apply_new(animal_id, user_id):
    sql = """
    INSERT INTO application (id, user_id, animal_id, date, state)
    VALUES (:id, :user_id, :animal_id, :date, :state)
    """
    id = len(db.engine.execute(text("select * from application")).fetchall()) + 1
    d= date.today().strftime("%x")
    db.engine.execute(text(sql).execution_options(autocommit=True),{'id': id, 'user_id':user_id,
                                        'animal_id':animal_id, 'date':d, 'state':'Submitted'})

def get_all_applications():
    sql = """
    SELECT *
    FROM application
    """
    applications = db.engine.execute(text(sql))
    return applications

def delete_animal_by_id(animal_id):
    sql = """
    DELETE
    FROM animal
    WHERE id = :x
    """
    db.engine.execute(text(sql).execution_options(autocommit=True),{'x': animal_id})

def delete_apply_by_id(animal_id):
    sql = """
    DELETE 
    FROM application
    WHERE animal_id = :x
    """
    db.engine.execute(text(sql).execution_options(autocommit=True),{'x': animal_id})

def get_submitted_apply():
    sql = """
    SELECT *
    FROM application
    WHERE state = 'Submitted'
    """
    applys = db.engine.execute(text(sql)).fetchall()
    return applys

def approve_apply(application_id):
    sql = """
    UPDATE application
    SET state = :s
    WHERE id = :a
    """
    db.engine.execute(text(sql).execution_options(autocommit=True),{'s': 'Approved', 'a':application_id})

def decline_apply(application_id):
    sql = """
    UPDATE application
    SET state = :s
    WHERE id = :a
    """
    db.engine.execute(text(sql).execution_options(autocommit=True),{'s': 'Declined', 'a':application_id})

def search_animals(color, cat, desexed, breed):
    sql = """
    SELECT *
    FROM animal
    WHERE color = :color and cat = :cat and desexed = :de and breed = :b
    """
    animals = db.engine.execute(text(sql), {'color':color, 'cat':cat, 'de':desexed, 'b':breed})
    return animals

def search_animal_by_name(name):
    sql = """
    SELECT *
    FROM animal
    WHERE name = :n
    """
    animals = db.engine.execute(text(sql), {'n': name}).fetchall()
    if animals:
        return True
    else:
        return False


def add_animal(name, cat, desexed, breed, color, weight, disease, picture):
    id = len(db.engine.execute(text("select * from animal")).fetchall()) + 1
    sql = """
    INSERT INTO animal (id, name, cat, desexed, breed, color, weight, disease, picture )
    VALUES (:id, :name, :cat, :desexed, :breed, :color, :weight, :disease, :picture)
    """
    db.engine.execute(text(sql).execution_options(autocommit=True),{'id': id, 'name':name,
                                        'cat':cat, 'desexed':desexed, 'breed':breed,
                                        'color':color, 'weight':weight, 'disease':disease,'picture':picture})

def change_password(id, n_hash):
    sql = """
    UPDATE adopter
    SET password_hash = :p
    WHERE id = :id
    """
    db.engine.execute(text(sql).execution_options(autocommit=True),{'p': n_hash, 'id':id})
