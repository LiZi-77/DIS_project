# Running the Web-App:

Assumes a working Python 3 installation (with python=python3 and pip=pip3).

(1) Run the code below to install the modules.

>$ pip install -r requirements.txt

(2) Database initialization.

1. set the serve, database, password, etc. in the __init__.py file.
    i.e. set in the line 6: app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/database' 

2. add forged data in the database by commands:

>$ flask initdb
>$ flask forge

(3) Run Web-App

>$ flask run

Note: All forged users with password abcd, and forged administrators with password dcba.


# About:
 ## (1) what the web-app can:
 The app for Animal Shelter provides access to everyone. But in order to achieve more, man should firstly create an account as either oridnary user or adiministrator via button SIGNUP. Then man can:

 a) As ordinary user:
 browse our inhabitant animals' pictures and more detailed information;
 search for your dream pet;
 apply to adopt a animal;
 check the applications you have made and see whether it is rejected or approved or waiting for a decision; 
 reset password;

 b) As administrator:
 browse our inhabitant animals' pictures and more detailed information;
 search for a pet;
 add a new inhabitant animal into the database;
 check the applications together with the corresponding applier and then make an approval or rejection; 
 reset password;

 ## (2) how the web-app can:
 The functions above are supported by four schemas:
animal: information on each animal;
user: information on each user;
application: information on applications, including attributes
             animal_id and user_id, which refer to schemas animal and user, respectively;
breed_description: information on some breeds


# Contributors:

Ying Pei, pwb749@alumni.ku.dk

JianPeng Zheng, cfv939@alumni.ku.dk

Ziqian Li, lkt692@alumni.ku.dk
