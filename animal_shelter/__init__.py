from flask import Flask
from flask_sqlalchemy import SQLAlchemy  
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:22055@localhost/animal_shelter'
app.config['SECRET_KEY'] = 'dev'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    from animal_shelter.models import User
    user = User.query.get(int(user_id)) 
    return user 

from animal_shelter import views, errors, commands
