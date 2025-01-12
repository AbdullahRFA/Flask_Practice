# Flask_Practice

The error occurs because Flask is not installed in your Python environment. To resolve this issue, follow these steps:

# 1. Install Flask

Run the following command in your terminal to install Flask:

        pip install flask

If you are using Python 3, ensure you use pip3:

        pip3 install flask

# 2. Verify Installation

Check if Flask is successfully installed by running:

        pip show flask

This should display information about the Flask package.

# 3. Use a Virtual Environment (Recommended)

To avoid conflicts between different projects, it’s a good idea to create a virtual environment for your project: 1. Create a virtual environment:

            python -m venv .venv

(Use python3 if you’re using Python 3.)

# 2. Activate the virtual environment:

• On macOS/Linux:

        source .venv/bin/activate

• On Windows:

        venv\Scripts\activate

# 3. Install Flask inside the virtual environment:

            pip install flask

# 4. Run the Flask Application

Once Flask is installed, you can run your Flask application with:

        python app.py

If the issue persists, let me know!

# 5. install all requirements

        pip install -r requirements.txt

# 6. install postman

        brew install --cask postman

# 7. instal Flask migrate

        pip install Flask-Migrate

# for my macbook

### I follow bellow procedure

         python -m venv .venv
         source .venv/bin/activate
         pip install -r requirements.txt
