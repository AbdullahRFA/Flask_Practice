from flask import Flask, request, jsonify
from config import Config
from model import student, db

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET'])
def get():
    students = student.query.all()
    return jsonify([
        {
            'id': s.id,
            'name': s.name,
            'email': s.email,
            "class_name": s.class_name,
            'admitted_at': s.admitted_at
        } for s in students
    ])

@app.route('/create/', methods=['POST'])
def create():
    name = request.form.get('name')
    email = request.form.get('email')
    class_name = request.form.get('class_name')

    if not name or not email or not class_name:
        return {"error": "All fields are required!"}, 400

    students = student(name=name, email=email, class_name=class_name)
    db.session.add(students)

    try:
        db.session.commit()
        return {"message": "Student created successfully!"}, 201
    except Exception as e:
        db.session.rollback()
        return {"error": f"Student could not be created. Error: {str(e)}"}, 500

@app.route('/edit/<int:id>', methods=['PUT'])
def edit(id):
    students = student.query.get_or_404(id)

    students.email = request.form.get('email', students.email)
    students.class_name = request.form.get('class_name', students.class_name)

    try:
        db.session.commit()
        return {"message": "Student updated successfully!"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": f"Failed to update student. Error: {str(e)}"}, 500

@app.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    students = student.query.get_or_404(id)

    try:
        db.session.delete(students)
        db.session.commit()
        return {"message": "Student deleted successfully!"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": f"Failed to delete student. Error: {str(e)}"}, 500

if __name__ == "__main__":
    app.run(debug=True)