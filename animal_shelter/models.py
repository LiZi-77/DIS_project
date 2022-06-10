from animal_shelter import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(db.Model, UserMixin):  
    id = db.Column(db.Integer, primary_key=True)  
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    type = db.Column(db.Boolean)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

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
    #user_id = db.Column(db.Integer)
    #animal_id = db.Column(db.Integer)
    #date = db.Column(db.String(20))
    breed = db.Column(db.String(50))
    details = db.Column(db.Text())