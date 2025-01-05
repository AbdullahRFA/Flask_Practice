import os

class Config:
    project_directory = os.path.abspath(os.path.dirname(__file__))
    # Ensure the directory exists
    os.makedirs(os.path.join(project_directory, 'data'), exist_ok=True)
    DATABASE_URI = 'sqlite:///' + os.path.join(project_directory, 'data', 'data.db')
    SQLALCHEMY_DATABASE_URI = DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Suppress warning messages