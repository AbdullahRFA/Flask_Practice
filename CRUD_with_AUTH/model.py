from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


# for authentications
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(60),nullable=False,unique=True)
    password = db.Column(db.String(100),nullable=False)
    
    
    
class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(60), unique=True)
    class_name = db.Column(db.String(60))
    admitted_at = db.Column(db.DateTime, default=datetime.now)
    
    def to_dict(self):
        return{
            'id': self.id,
            'name':self.name,
            'email':self.email,
            'class_name':self.class_name,
            'admitted_at':self.admitted_at.isoformat() if self.admitted_at else None
        }