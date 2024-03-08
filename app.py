from flask import Flask, request, flash, url_for, redirect, session, render_template, render_template_string
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

USERNAME = 'root'
PASSWORD = 'root'
HOST = 'localhost'
DB_NAME = 'database_name'  # replace

app = Flask(__name__, template_folder='website/templates', static_folder='website/static')

# app = Flask(__name__, template_folder='website/templates')

# # Static files (CSS, images, etc.)
# app.static_folder = 'static'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + USERNAME + ':' + PASSWORD + '@' + HOST + '/' + DB_NAME
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gym.sqlite3'
app.config['SECRET_KEY'] = 'root'
db = SQLAlchemy(app)

# Association table for many-to-many relationship between User and Class
booking = db.Table('booking',
                   db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                   db.Column('class_id', db.Integer, db.ForeignKey('class.id'), primary_key=True),
                   db.Column('booking_at', db.DateTime(timezone=True), default=func.now())
                   )


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    user_email = db.Column(db.String(120), unique=True, nullable=False)
    user_password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(120), nullable=False)
    # Relationship to Class through the bookings association table
    classes = db.relationship('Class', secondary=booking, back_populates='users')

    def __init__(self, first_name, last_name, user_email, user_password, role):
        self.first_name = first_name
        self.last_name = last_name
        self.user_email = user_email
        self.user_password = user_password
        self.role = role

    @classmethod
    def count_users(cls):
        return cls.query.count()


class Class(db.Model):
    __tablename__ = 'class'
    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(120), nullable=False)
    day = db.Column(db.String(120), nullable=False)
    time_duration = db.Column(db.String(500), nullable=False)
    # Relationship to User through the bookings association table
    users = db.relationship('User', secondary=booking, back_populates='classes')


def create_tables():
    db.create_all()


def add_initial_data():
    # Create initial users if one already doesn't exist
    if db.session.query(User).count() == 0:
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

@app.route('/')
def index():
    # Check if the user is logged in by looking for 'user_id' in session
    if 'user_id' in session:
        # Get the user's details from the database
        user = User.query.get(session['user_id'])
        # Check the first login flag
        if session.get('first_login'):
            # Since we've already shown 'Login successful', now we set it to False
            session['first_login'] = False
        else:
            flash('Welcome back {}!'.format(user.first_name), 'info')
        return render_template('index.html', user=user)
    else:
        # If user is not logged in, just render the index page
        return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'Login' in request.form:
        user_email = request.form['user_email']
        user_password = request.form['user_password']

        # Find user with the provided email and password
        user = db.session.query(User).filter_by(user_email=user_email, user_password=user_password).first()
        if user:
            # Set session
            session['user_id'] = user.id
            # Check if it's the user's first login by checking a flag in session
            if 'first_login' not in session:
                # Set the first login flag
                session['first_login'] = True
                flash('Login successful!', 'success')
            else:
                session['first_login'] = False
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
        required_fields = ['first_name', 'last_name', 'user_email', 'user_password']
        for field in required_fields:
            if not request.form.get(field):
                alert_message = 'Please fill in all fields.'
                return render_template('register.html', alert=alert_message, alert_type='error')

        # Check if the email already exists
        user_exists = db.session.query(User).filter_by(user_email=request.form['user_email']).first()
        if user_exists:
            alert_message = 'User with email "{0}" already exists. Please log in.'.format(user_exists)
            return render_template('login.html', alert=alert_message, alert_type='info')

        # Create a new user
        new_user = User(
            first_name=request.form['first_name'],
            last_name=request.form['last_name'],
            user_email=request.form['user_email'],
            user_password=request.form['user_password'],
            role=request.form['role']
        )
        # Add new user to the db
        db.session.add(new_user)
        db.session.commit()
        # Redirect to login page with success message
        return redirect(url_for('login', success_message='Registration successful. Please log in.'))
    return render_template('register.html', users_count=users_count_value)


@app.route('/logout')
def logout():
    # Remove 'user_id' from session
    session.pop('user_id', None)
    # You may want to flash a message confirming the user has logged out
    flash('You have been logged out.', 'success')
    # Redirect to index page or login page
    return redirect(url_for('index'))


@app.route('/booking')
def booking():
    return render_template('booking.html')


@app.route('/create-class', methods=['GET', 'POST'])
def create_class():
    if request.method == 'POST':
        # Retrieve form data
        class_name = request.form['class_name']
        day = request.form['day']
        time_duration = request.form['time_duration']

        # Create a new Class instance
        new_class = Class(class_name=class_name, day=day, time_duration=time_duration)

        # Add the new class to the session and commit it to the database
        db.session.add(new_class)
        db.session.commit()

        # Flash a success message
        flash('Class created successfully!', 'success')

        # Redirect to the class listing page (booking)
        return redirect(url_for('index'))

    # For a GET request, just render the class creation form
    return render_template('create_class.html')


if __name__ == '__main__':
    create_tables()
    add_initial_data()
    app.run(debug=True)
