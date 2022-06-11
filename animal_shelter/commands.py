from animal_shelter import app, db
from animal_shelter.models import Breed_description, User, Animal, Application
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
    db.create_all()
    click.echo('Initialized database.')

@app.cli.command()
def forge():
    """Generate fake data."""
    db.drop_all()
    db.create_all()
    disease_description = 'Totally healthy'
    animals = [
        {'name': 'Kitty', 'cat': True,  'desexed': False, 'breed':'Abyssinian',
         'color': 'brown', 'weight': 12.00, 'disease': disease_description, 
         'picture': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/Gustav_chocolate.jpg/800px-Gustav_chocolate.jpg'},
        {'name': 'Mimi', 'cat': True,  'desexed': True, 'breed': 'American Shorthair', 
        'color': 'gray', 'weight': 10.00, 'disease': disease_description, 
        'picture': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/14_years_old_american_shorthair.jpg/800px-14_years_old_american_shorthair.jpg'},
        {'name': 'Leopard', 'cat': True,  'desexed': True, 'breed': 'Egyptian Mau', 
        'color': 'patterned', 'weight': 10.00, 'disease': disease_description, 
        'picture': 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Egyptian_Mau_Bronze.jpg/1280px-Egyptian_Mau_Bronze.jpg'},
        {'name': 'Meatball', 'cat': True,  'desexed': True, 'breed': 'Oriental', 
        'color': 'black', 'weight': 14.00, 'disease': disease_description, 
        'picture': 'https://cdn.w600.comps.canstockphoto.com/black-oriental-shorthair-cat-portrait-stock-images_csp76652853.jpg'},
   
        {'name': 'Fox', 'cat': False,  'desexed': False, 'breed': 'Alaskan Malamute', 
        'color': 'patterned', 'weight': 20.00, 'disease': disease_description, 
        'picture': 'https://upload.wikimedia.org/wikipedia/commons/9/9f/Alaskan_Malamute.jpg'},
        {'name': 'Wood', 'cat': False,  'desexed': True, 'breed': 'American Water Spaniel', 'color': 'brown', 'weight': 20.00, 'disease': disease_description, 
        'picture': 'https://upload.wikimedia.org/wikipedia/commons/5/5a/Chien_d%27eau_americain_champion_1.JPG'},
        {'name': 'Bertram', 'cat': False,  'desexed': True, 'breed': 'Samoyed', 
        'color': 'white', 'weight': 19.00, 'disease': disease_description, 
        'picture': 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/Samojed00.jpg/1024px-Samojed00.jpg'},
        {'name': 'Pippi', 'cat': False,  'desexed': False, 'breed': 'Chihuahua', 
        'color': 'gray', 'weight': 11.00, 'disease': disease_description, 
        'picture': 'https://www.anicura.dk/globalassets/group/breed-tool/images-dogs/chihuahua.jpg'},
         {'name': 'Kiki', 'cat': False,  'desexed': True, 'breed': 'Bolognese', 
        'color': 'white', 'weight': 18.00, 'disease': disease_description, 
        'picture': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQMrW351iRpq1SqLNpfqAQXwqqf8JX8HLsOFA&usqp=CAU'}
    ]

    for a in animals:
        animal = Animal(name=a['name'],cat=a['cat'], desexed=a['desexed'],
         breed=a['breed'], color=a['color'], weight=a['weight'], 
         disease=a['disease'], picture=a['picture'])
        db.session.add(animal)
    
    db.session.commit()
    click.echo('Some forged animals are added into database ')


    #False for user, i.e. potential adopters, True for shelter administrators
    mobile1, mobile2, mobile3 = '50133333','50144444','50155555'
    occuption='professor'
    post=4000
    users = [
        {'username':'Tom', 'password_hash': generate_password_hash('abcd'),'type':False,'mobile':mobile1, 
        'gender':False, 'age':56,'occupation':occuption,'post':post},
        {'username':'Peter', 'password_hash': generate_password_hash('abcd'),'type':False,'mobile':mobile3,
        'gender':False, 'age':59,'occupation':occuption,'post':post},
        {'username':'Jerry', 'password_hash':generate_password_hash('abcd'),'type':False,'mobile':mobile1,
        'gender':False, 'age':66,'occupation':occuption,'post':post},
        {'username':'Henry', 'password_hash': generate_password_hash('abcd'),'type':False,'mobile':mobile2,
        'gender':False, 'age':25,'occupation':occuption,'post':post},
        {'username':'Jakob', 'password_hash': generate_password_hash('abcd'),'type':False,'mobile':mobile2,
        'gender':False, 'age':16,'occupation':occuption,'post':post},
        {'username':'Monica', 'password_hash': generate_password_hash('abcd'),'type':False,'mobile':mobile1,
        'gender':True, 'age':13,'occupation':occuption,'post':post},
        {'username':'admin1', 'password_hash': generate_password_hash('dcba'),'type':True,'mobile':mobile3,
        'gender':False, 'age':34,'occupation':occuption,'post':post},
        {'username':'admin2', 'password_hash': generate_password_hash('dcba'),'type':True,'mobile':mobile3,
        'gender':True, 'age':54,'occupation':occuption,'post':post},
        {'username':'admin3', 'password_hash': generate_password_hash('dcba'),'type':True,'mobile':mobile3,
        'gender':False, 'age':36,'occupation':occuption,'post':post}
    ]
    for u in users:
        user=User(username=u['username'], password_hash=u['password_hash'], type=u['type'], 
        mobile=u['mobile'],gender=u['gender'],age=u['age'], occupation=u['occupation'],post=u['post'])
        db.session.add(user)
    db.session.commit()
    click.echo('Some forged users are added into database')


    applications = [
        {'user_id': 3, 'animal_id':6, 'date': '03/06/21','state':'Approved'},
        {'user_id': 4, 'animal_id':2, 'date': '04/04/21','state':'Declined'},
        {'user_id': 3, 'animal_id':2, 'date': '04/04/21','state':'Submitted'}

       ]
    for a in applications:
        application=Application(user_id=a['user_id'], animal_id=a['animal_id'], 
        date=a['date'], state=a['state'])
        db.session.add(application)
    db.session.commit()
    click.echo('Some forged applications are added into database')


    breed_descriptions = [
            {'breed': 'Abyssinian', 
             'detail':'https://en.wikipedia.org/wiki/Abyssinian_cat'},
            {'breed': 'American_Shorthair',
             'detail':'https://en.wikipedia.org/wiki/American_Shorthair'},
             {'breed': 'Egyptian Mau',
             'detail':'https://en.wikipedia.org/wiki/Egyptian_Mau'},
            {'breed': 'Oriental',
             'detail': 'https://en.wikipedia.org/wiki/Oriental_Shorthair'},
              {'breed': 'Persian',
             'detail':'https://en.wikipedia.org/wiki/Persian_cat'},
             {'breed': 'Alaskan Malamute',
             'detail':'https://da.wikipedia.org/wiki/Alaskan_malamute'},
             {'breed': 'American Water Spaniel',
             'detail':'https://en.wikipedia.org/wiki/American_Water_Spaniel'},
             {'breed': 'Samoyed',
             'detail':'https://en.wikipedia.org/wiki/Samoyed_dog'},
             {'breed': 'Labrador Retriever',
             'detail':'https://en.wikipedia.org/wiki/Labrador_Retriever'},
             {'breed': 'Chihuahua',
             'detail': 'https://en.wikipedia.org/wiki/Chihuahua_(dog)'},
             {'breed': 'Bolognese',
             'detail': 'https://en.wikipedia.org/wiki/Bolognese_(dog)'}
             ]
    for b in breed_descriptions:
        desc=Breed_description(breed=b['breed'], details=b['detail'])
        db.session.add(desc)
    db.session.commit()
    click.echo('Some breed descriptions are added into database')





