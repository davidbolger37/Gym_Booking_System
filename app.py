from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum

USERNAME = 'root'
PASSWORD = 'root'
HOST = 'localhost'
DB_NAME = 'database_name'  # replace

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + USERNAME + ':' + PASSWORD + '@' + HOST + '/' + DB_NAME
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class UserRole(Enum):
    ADMIN = 'admin'
    USER = 'user'

class User(db.Model):
    __tablename__ = 'user_table'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    user_email = db.Column(db.String(120), unique=True, nullable=False)
    user_password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False)

    def __init__(self, first_name, last_name, user_email, user_password, role):
        self.first_name = first_name
        self.last_name = last_name
        self.user_email = user_email
        self.user_password(user_password)
        self.role = role

    @classmethod
    def count_users(cls):
        return cls.query.count()


# @app.route('/')
# def hello():
#     return 'Hello!'


@app.route('/login')
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
