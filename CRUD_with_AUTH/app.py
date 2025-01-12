from flask import Flask, request, jsonify, session
from config import Config
from model import db, Students, User
from auth_check import has_password, verify_password
from functools import wraps  # Import wraps to preserve function names
import os
app = Flask(__name__)
app.config.from_object(Config)
# Set a secret key
app.secret_key = os.urandom(24)  # Or set a fixed key for production

db.init_app(app)

with app.app_context():
    db.create_all()


# Middleware for login-required functionality
def login_required(f):
    @wraps(f)  # Use wraps to preserve the function's metadata
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({"Error": "Please log in first"}), 401
        return f(*args, **kwargs)
    return decorated_function


# User registration
@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return jsonify({"Error": "Username and password are required"}), 400

    # Hash the password and save the user
    user = User(username=username, password=has_password(password))
    db.session.add(user)

    try:
        db.session.commit()
        return jsonify({"message": "User registered successfully!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"Error": f"User could not be created: {str(e)}"}), 500


# User login
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    # Retrieve user from database
    user = User.query.filter_by(username=username).first()

    if user and verify_password(user.password, password):
        session['user_id'] = user.id
        return jsonify({"message": "Login successful"}), 200

    return jsonify({"Error": "Invalid credentials"}), 401


# User logout
@app.route('/logout', methods=['GET'])
def logout():
    session.pop('user_id', None)
    return jsonify({"message": "Logout successful"}), 200


# Get all students
@app.route('/', methods=['GET'])
@login_required
def get_student_data():
    students = Students.query.all()
    return jsonify([student.to_dict() for student in students]), 200


# Create a new student
@app.route('/create', methods=['POST'])
@login_required
def create_student():
    name = request.form.get('name')
    email = request.form.get('email')
    class_name = request.form.get('class_name')

    if not name or not email or not class_name:
        return jsonify({"Error": "All fields are required"}), 400

    # Add new student to the database
    student = Students(name=name, email=email, class_name=class_name)
    db.session.add(student)

    try:
        db.session.commit()
        return jsonify({"message": "Student created successfully!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"Error": f"Student could not be created: {str(e)}"}), 500


# Update student details
@app.route('/edit/<int:id>', methods=['PUT'])
@login_required
def edit(id):
    student = Students.query.get_or_404(id)

    student.email = request.form.get('email', student.email)
    student.class_name = request.form.get('class_name', student.class_name)

    try:
        db.session.commit()
        return jsonify({"message": "Student updated successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"Error": f"Failed to update student: {str(e)}"}), 500


# Delete a student
@app.route('/delete/<int:id>', methods=['DELETE'])
@login_required
def delete(id):
    student = Students.query.get_or_404(id)

    try:
        db.session.delete(student)
        db.session.commit()
        return jsonify({"message": "Student deleted successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"Error": f"Student could not be deleted: {str(e)}"}), 500


# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)