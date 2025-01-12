from flask import Flask, request, redirect, flash, jsonify
from config import Config
from model import db, Students

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET'])
def get_student_data():
    students = Students.query.all()  # Change variable name from 'student' to 'students'
    # return jsonify([{
    #     "id": s.id,
    #     "name": s.name,
    #     "email": s.email,
    #     "class_name": s.class_name,
    #     "admitted_at": s.admitted_at
    # } for s in students])  # Use 'students' here
    
    return jsonify([student.to_dict() for student in students])

@app.route('/create', methods=['POST'])
def create_student():
    name = request.form.get('name')
    email = request.form.get('email')
    class_name = request.form.get('class_name')
    
    if not name or not email or not class_name:
        return {"Error": "All fields are required"}, 400  # Add a status code for bad request
    
    student = Students(name=name, email=email, class_name=class_name)
    db.session.add(student)
    
    try:
        db.session.commit()
        return {"message": "Student created successfully!"}, 201
    except Exception as e:
        db.session.rollback()
        return {"Error": f"Student could not be created: {str(e)}"}, 500  # Fixed error message formatting

@app.route('/edit/<int:id>', methods=['PUT'])
def edit(id):
    student = Students.query.get_or_404(id)

    student.email = request.form.get('email', student.email)
    student.class_name = request.form.get('class_name', student.class_name)

    try:
        db.session.commit()
        return {"message": "Student updated successfully!"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": f"Failed to update student. Error: {str(e)}"}, 500

@app.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    student = Students.query.get_or_404(id)
    
    try:
        db.session.delete(student)
        db.session.commit()
        return {"message": "Student deleted successfully!"}, 200  # Fixed spelling of 'message'
    except Exception as e:
        db.session.rollback()
        return {"Error": f"Student could not be deleted: {str(e)}"}, 500  # Fixed error message

if __name__ == "__main__":
    app.run(debug=True)