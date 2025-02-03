from unittest import TestCase

from app import app
from models import db, User


app.config['SQLALCHEMY_DATABASE_URL'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()


    
    
    