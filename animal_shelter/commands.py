from animal_shelter import app, db
from animal_shelter.models import User, Animal, Application
import click


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    db.session.commit()
    if drop:
        db.drop_all()
        click.echo('Deleted database.')
    
    db.create_all()
    click.echo('Initialized database.')

@app.cli.command()
def forge():
    """Generate fake data."""
    db.drop_all()
    db.create_all()

    disease_description = 'Totally healthy'
    animals = [
        {'name': 'cat1', 'cat': True, 'breed': 'Abyssinian', 'color': 'yellow', 'weight': 12.00, 'disease': disease_description},
        {'name': 'cat2', 'cat': True, 'breed': 'American Shorthair', 'color': 'blue', 'weight': 10.00, 'disease': disease_description},
        {'name': 'cat3', 'cat': True, 'breed': 'Egyptian Mau', 'color': 'white', 'weight': 10.00, 'disease': disease_description},
        {'name': 'dog1', 'cat': False, 'breed': 'ardedDog', 'color': 'black', 'weight': 20.00, 'disease': disease_description},
        {'name': 'dog1', 'cat': False, 'breed': 'ardedDog', 'color': 'black', 'weight': 20.00, 'disease': disease_description},
        {'name': 'dog2', 'cat': False, 'breed': 'American Water Spaniel', 'color': 'white', 'weight': 20.00, 'disease': disease_description},
        {'name': 'dog3', 'cat': False, 'breed': 'Samoyed', 'color': 'white', 'weight': 20.00, 'disease': disease_description},
    ]

    for a in animals:
        animal = Animal(name=a['name'],cat=a['cat'], breed=a['breed'], color=a['color'], weight=a['weight'], disease=a['disease'])
        db.session.add(animal)
    
    db.session.commit()
    click.echo('Done.')





