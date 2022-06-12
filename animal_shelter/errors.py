from animal_shelter import app
from flask import render_template

@app.errorhandler(500) 
def page_not_found(e): 
    from animal_shelter.models import Adopter
    user = Adopter.query.first()
    return render_template('500.html', user=user), 500  