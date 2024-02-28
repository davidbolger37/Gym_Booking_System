from flask import Flask, request, flash, url_for, redirect, session, render_template, render_template_string
from flask_sqlalchemy import SQLAlchemy

USERNAME = 'root'
PASSWORD = 'root'
HOST = 'localhost'
DB_NAME = 'database_name'  # replace

app = Flask(__name__, template_folder='website/templates')

# Static files (CSS, images, etc.)
app.static_folder = 'static'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + USERNAME + ':' + PASSWORD + '@' + HOST + '/' + DB_NAME
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gym.sqlite3'
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user_table'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    user_email = db.Column(db.String(120), nullable=False)
    user_password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(120), nullable=False)

    def __init__(self, first_name, last_name, user_email, user_password, role):
        self.first_name = first_name
        self.last_name = last_name
        self.user_email = user_email
        self.user_password = user_password
        self.role = role

    @classmethod
    def count_users(cls):
        return cls.query.count()


def create_tables():
    db.create_all()


def add_initial_data():
    # Create initial users and dogs
    if db.session.query(User).count() == 0:
        # Create initial users and dogs
        user1 = User(first_name='user1', last_name="user1", user_email='user1@gmail.com', user_password='user1',
                     role="user")
        user2 = User(first_name='user2', last_name="user2", user_email='user2@gmail.com', user_password='user2',
                     role="user")
        user3 = User(first_name='user3', last_name="user3", user_email='user3@gmail.com', user_password='user3',
                     role="user")
        user4 = User(first_name='user4', last_name="user4", user_email='user4@gmail.com', user_password='user4',
                     role="user")
        user5 = User(first_name='user5', last_name="user5", user_email='user5@gmail.com', user_password='user5',
                     role="user")
        user6 = User(first_name='user6', last_name="user6", user_email='user6@gmail.com', user_password='user6',
                     role="user")
        users = [user1, user2, user3, user4, user5, user6]
        db.session.add_all(users)
        db.session.commit()


###################################################
#                    ROUTES                       #
###################################################
# @app.route('/')
# def hello():
#     return 'Hello!'


@app.route('/', methods=['GET', 'POST'])
def login():
    if 'Login' in request.form:
        user_email = request.form['user_email']
        user_password = request.form['user_password']

        # Find user with the provided email and password
        user = db.session.query(User).filter_by(user_email=user_email, user_password=user_password).first()
        if user:
            # Set session
            session['user_id'] = user.id
            # flash('Login successful !', 'success')
            return redirect(url_for('index'))
        else:
            alert_message = "Invalid email or password, please try again."
            return render_template('login.html', alert=alert_message, alert_type='error')
            # flash('Invalid email or password', 'error')
    elif 'Register' in request.form:
        return redirect(url_for('register'))
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    # Calling class methods to get counts
    users_count_value = User.count_users()

    if request.method == 'POST':
        # Validate required fields are filled
        required_fields = ['user', 'user_email', 'user_password']
        for field in required_fields:
            if not request.form.get(field):
                flash(f'Flash register() error\nPlease enter {field}', 'error')
                return redirect(url_for('register'))

        # Check if the email already exists
        user_exists = db.session.query(User).filter_by(user_email=request.form['user_email']).first()
        if user_exists:
            alert_message = 'User with email "{0}" already exists. Please log in.'.format(user_exists)
            return render_template_string('login.html', alert=alert_message, alert_type='info')

        # Create a new user
        new_user = User(
            first_name=request.form['first_name'],
            last_name=request.form['last_name'],
            user_email=request.form['user_email'],
            user_password=request.form['user_password'],
            role = request.form['role']
        )
        # Add new user to the db
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login', success_message='200'))
    return render_template('register.html', users_count=users_count_value, dogs_count=dogs_count_value)


if __name__ == '__main__':
    create_tables()
    add_initial_data()
    app.run(debug=True)
