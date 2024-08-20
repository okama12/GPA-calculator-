from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gpa_calculator.db'
app.config['SECRET_KEY'] = '1263764474747547'
db = SQLAlchemy(app)

from app import routes

with app.app_context():
    db.create_all()
    