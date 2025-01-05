# REST API
# Representational state transfer application programable interface
'''
CRUD
1. Create
2. Read
3. Update
4. Delete
'''
from config import Config
from models import db, Student
from flask import Flask, request, redirect,flash
'''
The Flask class is the central object in the Flask framework.
app is the instance of the Flask class that represents your web application.
__name__ is a special Python variable that contains the name of the current module.
'''
app = Flask(__name__)

'''
This app object is used to define routes, handle requests, 
and manage the application’s configuration and behavior.
'''
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET'])
def get_data():
    students = Student.query.all()
    result = [
        {"id": s.id, "name": s.name, "email": s.email, "class_name": s.class_name, "admitted_at": s.admitted_at}
        for s in students
    ]
    return {"students": result}, 200

@app.route('/create', methods=['POST'])
def create():
    name = request.form.get('name', '')
    email = request.form.get('email', '')
    class_name = request.form.get('class_name', '')

    if not name or not email or not class_name:
        return {"error": "All fields are required"}, 400

    student = Student(name, email, class_name)
    db.session.add(student)

    try:
        db.session.commit()
        return {"message": "Student created successfully!"}, 201
    except:
        db.session.rollback()
        return {"error": "Student could not be created!"}, 500

@app.route('/edit/<int:id>', methods=['PUT'])
def edit(id):
    student = Student.query.get(id)
    if not student:
        return {"error": "Student not found"}, 404

    name = request.form.get('name', student.name)
    email = request.form.get('email', student.email)
    class_name = request.form.get('class_name', student.class_name)

    student.name = name
    student.email = email
    student.class_name = class_name

    try:
        db.session.commit()
        return {"message": "Student updated successfully!"}, 200
    except:
        db.session.rollback()
        return {"error": "Student could not be updated!"}, 500

@app.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    student = Student.query.get(id)
    if not student:
        return {"error": "Student not found"}, 404

    db.session.delete(student)
    db.session.commit()
    return {"message": "Student deleted successfully!"}, 200

if __name__ == "__main__":
    app.run(debug=True)