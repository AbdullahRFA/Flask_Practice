from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_there():
    return "Hello Flask"
@app.route("/admin")
def admin():
    return "This Abdullah Nazmus-Sakib"
if __name__ == "__main__":
    app.run(debug=True)