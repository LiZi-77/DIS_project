from animal_shelter import app, db
from animal_shelter.models import User, Animal, Application
from werkzeug.security import generate_password_hash
import click


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    db.session.commit()
    if drop:
        db.drop_all()
        click.echo('Deleted database.')
    print('qqqq')
    db.create_all()
    click.echo('Initialized database.')

@app.cli.command()
def forge():
    """Generate fake data."""
    db.drop_all()
    db.create_all()
    disease_description = 'Totally healthy'
    animals = [
        {'name': 'cat1', 'cat': True, 'breed': 'Abyssinian', 'color': 'yellow', 'weight': 12.00, 'disease': disease_description, 'picture': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/Gustav_chocolate.jpg/800px-Gustav_chocolate.jpg'},
        {'name': 'cat2', 'cat': True, 'breed': 'American Shorthair', 'color': 'blue', 'weight': 10.00, 'disease': disease_description, 'picture': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/14_years_old_american_shorthair.jpg/800px-14_years_old_american_shorthair.jpg'},
        {'name': 'cat3', 'cat': True, 'breed': 'Egyptian Mau', 'color': 'white', 'weight': 10.00, 'disease': disease_description, 'picture': 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Egyptian_Mau_Bronze.jpg/1280px-Egyptian_Mau_Bronze.jpg'},
        {'name': 'dog1', 'cat': False, 'breed': 'Alaskan Malamute', 'color': 'black', 'weight': 20.00, 'disease': disease_description, 'picture': 'https://upload.wikimedia.org/wikipedia/commons/9/9f/Alaskan_Malamute.jpg'},
        {'name': 'dog2', 'cat': False, 'breed': 'American Water Spaniel', 'color': 'white', 'weight': 20.00, 'disease': disease_description, 'picture': 'https://upload.wikimedia.org/wikipedia/commons/5/5a/Chien_d%27eau_americain_champion_1.JPG'},
        {'name': 'dog3', 'cat': False, 'breed': 'Samoyed', 'color': 'white', 'weight': 20.00, 'disease': disease_description, 'picture': 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/Samojed00.jpg/1024px-Samojed00.jpg'},
    ]

    for a in animals:
        animal = Animal(name=a['name'],cat=a['cat'], breed=a['breed'], color=a['color'], weight=a['weight'], disease=a['disease'], picture=a['picture'])
        db.session.add(animal)
    
    db.session.commit()
    click.echo('Some forged animals are added into database ')


    #False for user, i.e. potential adopters, True for shelter administrators
    users = [
        {'username':'Tom', 'password_hash': generate_password_hash('abcd'),'type':False},
        {'username':'Peter', 'password_hash': generate_password_hash('abcd'),'type':False},
        {'username':'Jerry', 'password_hash':generate_password_hash('abcd'),'type':False},
        {'username':'Henry', 'password_hash': generate_password_hash('abcd'),'type':False},
        {'username':'Jakob', 'password_hash': generate_password_hash('abcd'),'type':False},
        {'username':'Lily', 'password_hash': generate_password_hash('abcd'),'type':False},
        {'username':'Anna', 'password_hash': generate_password_hash('abcd'),'type':False},
        {'username':'Monica', 'password_hash': generate_password_hash('abcd'),'type':False},
        {'username':'Soft kitty', 'password_hash': generate_password_hash('dcba'),'type':True},
        {'username':'Warm kitty', 'password_hash': generate_password_hash('dcba'),'type':True},
        {'username':'Fur ball', 'password_hash': generate_password_hash('dcba'),'type':True}
    ]
    for u in users:
        user=User(username=u['username'], password_hash=u['password_hash'], type=u['type'])
        db.session.add(user)
    db.session.commit()
    click.echo('Some forged users are added into database')


    applications = [
        {'user_id': 3, 'animal_id':6, 'date': '03/06/2021','state':'Approved'},
        {'user_id': 4, 'animal_id':2, 'date': '04/04/2021','state':'Declined'},
       ]
    for a in applications:
        application=Application(user_id=a['user_id'], animal_id=a['animal_id'], 
        date=a['date'], state=a['state'])
        db.session.add(application)
    db.session.commit()
    click.echo('Some forged applications are added into database')





