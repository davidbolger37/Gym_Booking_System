from flask import Flask, request, flash, url_for, redirect, session, render_template, render_template_string
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy.exc import IntegrityError

USERNAME = 'root'
PASSWORD = 'root'
HOST = 'localhost'
DB_NAME = 'database_name'  # replace

app = Flask(__name__, template_folder='website/templates', static_folder='website/static')

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


def add_admin():
    # Check if an admin user already exists
    admin_exists = User.query.filter_by(role='admin').first()
    if not admin_exists:
        admin = User(
            first_name='admin',
            last_name='admin',
            user_email='admin@example.com',
            user_password='admin',
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()


# def reset_classes():
#     db.session.query(Class).delete()
#     db.session.commit()
#
#     db.session.execute("VACUUM")
#     db.session.commit()


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
            flash('Welcome {}!'.format(user.first_name), 'info')
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
            session['user_role'] = user.role  # Store user role in session
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
    user_role = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        user_role = user.role
    # Fetch all classes and sort them by day
    classes = Class.query.all()
    classes_by_day = {}
    for class_ in classes:
        if class_.day not in classes_by_day:
            classes_by_day[class_.day] = []
        classes_by_day[class_.day].append(class_)
    return render_template('booking.html', user_role=user_role, classes_by_day=classes_by_day)


@app.route('/create-class', methods=['GET', 'POST'])
def create_class():
    if 'user_id' not in session or session.get('user_role') != 'admin':
        # If the user is not logged in or not an admin, redirect them
        flash('You do not have permission to access this page.', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Retrieve form data
        class_name = request.form.get('class_name')
        day = request.form.get('day')
        time_duration = request.form.get('time_duration')

        # Check if the class already exists to prevent duplicates
        existing_class = Class.query.filter_by(class_name=class_name, day=day, time_duration=time_duration).first()

        if existing_class:
            flash('Class already exists.', 'error')
            return redirect(url_for('create_class'))

        # Create a new Class instance if it doesn't exist
        try:
            new_class = Class(class_name=class_name, day=day, time_duration=time_duration)
            db.session.add(new_class)
            db.session.commit()
            flash('Class created successfully!', 'success')
        except IntegrityError:
            db.session.rollback()
            flash('An error occurred while creating the class.', 'error')

        # Redirect to the class listing page (booking)
        return redirect(url_for('booking'))

    # For a GET request, just render the class creation form
    return render_template('create_class.html')


@app.route('/update-class/<int:class_id>', methods=['GET', 'POST'])
def update_class(class_id):
    if 'user_id' not in session or session.get('user_role') != 'admin':
        # If the user is not logged in or not an admin, redirect them
        flash('You do not have permission to access this page.', 'error')
        return redirect(url_for('login'))

    # Retrieve the class from the database
    class_to_update = Class.query.get_or_404(class_id)

    if request.method == 'POST':
        # Retrieve form data
        class_name = request.form.get('class_name')
        day = request.form.get('day')
        time_duration = request.form.get('time_duration')

        # Check if the class already exists to prevent duplicates
        existing_class = Class.query.filter_by(class_name=class_name, day=day, time_duration=time_duration).first()

        if existing_class:
            flash('A class with the same name, day, and time already exists.', 'error')
            return redirect(url_for('update_class', class_id=class_id))

        # Update the Class instance if it already doesn't exist
        try:
            class_to_update.class_name = class_name
            class_to_update.day = day
            class_to_update.time_duration = time_duration
            db.session.commit()
            flash(f'Class:{class_name} updated successfully!', 'success')
        except IntegrityError:
            db.session.rollback()
            flash('An error occurred while updating the class.', 'error')

        # Redirect to the class listing page (booking)
        return redirect(url_for('booking'))

    # For a GET request, just render the class update form
    return render_template('update_class.html', class_=class_to_update)


if __name__ == '__main__':
    create_tables()
    add_initial_data()
    add_admin()
    # reset_classes()
    app.run(debug=True)
