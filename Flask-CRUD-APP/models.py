from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Student(db.Model):  # Inherit from db.Model
    __tablename__ = 'students'  # Explicit table name (optional)
    
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    name = db.Column(db.String(100), nullable=False)  # Name (required)
    email = db.Column(db.String(60), unique=True, nullable=False)  # Unique email
    class_name = db.Column(db.String(60))  # Class name
    admitted_at = db.Column(db.DateTime, default=datetime.now)  # Default value for datetime
    
    def __init__(self, name, email, class_name):
        self.name = name
        self.email = email
        self.class_name = class_name