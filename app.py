from flask import Flask, request, flash, url_for, redirect, session, render_template, render_template_string
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy import Enum, case
import re

USERNAME = 'root'
PASSWORD = ''
HOST = 'localhost'
DB_NAME = 'gym_db'

app = Flask(__name__, template_folder='website/templates', static_folder='website/static')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + USERNAME + ':' + PASSWORD + '@' + HOST + '/' + DB_NAME
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'root'
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(40), nullable=False)
    last_name = db.Column(db.String(40), nullable=False)
    user_email = db.Column(db.String(255), unique=True, nullable=False)
    user_password = db.Column(db.String(255), nullable=False)
    role = db.Column(Enum('user', 'admin'), nullable=False)
    bookings = db.relationship('Booking', back_populates='user', cascade="all, delete-orphan")

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
    class_name = db.Column(db.String(40), nullable=False)
    day = db.Column(db.String(15), nullable=False)
    time_duration = db.Column(db.String(40), nullable=False)
    bookings = db.relationship('Booking', back_populates='class_', cascade="all, delete-orphan")

    def __init__(self, class_name, day, time_duration):
        self.class_name = class_name
        self.day = day
        self.time_duration = time_duration


class Booking(db.Model):
    __tablename__ = 'booking'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id', ondelete='CASCADE'), nullable=False)
    booking_at = db.Column(db.DateTime(timezone=True), default=db.func.now())

    # Additional columns to store email and class names
    user_email = db.Column(db.String(255), nullable=False)
    class_name = db.Column(db.String(40), nullable=False)
    day = db.Column(db.String(15), nullable=False)
    time_duration = db.Column(db.String(40), nullable=False)

    user = db.relationship('User', back_populates='bookings')
    class_ = db.relationship('Class', back_populates='bookings')

    def __init__(self, user_id, class_id, user_email, class_name, day, time_duration):
        self.user_id = user_id
        self.class_id = class_id
        self.user_email = user_email
        self.class_name = class_name
        self.day = day
        self.time_duration = time_duration


###################################################
#                    ROUTES                       #
###################################################


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
    user_id = None
    user = None

    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user:
            user_role = user.role
            user_id = user.id

        # Define an ordering for the days of the week using positional arguments for "whens"
        day_ordering = case(
            (Class.day == 'Monday', 1),
            (Class.day == 'Tuesday', 2),
            (Class.day == 'Wednesday', 3),
            (Class.day == 'Thursday', 4),
            (Class.day == 'Friday', 5),
            (Class.day == 'Saturday', 6),
        )

    # Fetch all classes and order them first by day, then by time_duration
    classes = Class.query.order_by(day_ordering, Class.time_duration).all()

    classes_by_day = {}
    for class_ in classes:
        if class_.day not in classes_by_day:
            classes_by_day[class_.day] = []
        classes_by_day[class_.day].append(class_)

    # Fetch all bookings
    bookings = Booking.query.all()

    return render_template('booking.html', user=user, user_id=user_id, user_role=user_role, classes_by_day=classes_by_day,
                           bookings=bookings)


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

        # Regex pattern for matching "11:00 AM - 12:00 PM" format
        pattern = r'^(?:1[0-2]|0?[1-9]):[0-5][0-9] [AP]M - (?:1[0-2]|0?[1-9]):[0-5][0-9] [AP]M$'

        # Server-side validation of the time slot format
        if not re.match(pattern, time_duration):
            flash('Invalid time slot format. Please use the "11:00 AM - 12:00 PM" format.', 'error')
            return render_template('create_class.html')

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

        # Regex pattern for matching "11:00 AM - 12:00 PM" format
        pattern = r'^(?:1[0-2]|0?[1-9]):[0-5][0-9] [AP]M - (?:1[0-2]|0?[1-9]):[0-5][0-9] [AP]M$'

        # Server-side validation of the time slot format
        if not re.match(pattern, time_duration):
            flash('Invalid time slot format. Please use the "11:00 AM - 12:00 PM" format.', 'error')
            return render_template('create_class.html')

        # Check if the class already exists to prevent duplicates
        existing_class = Class.query.filter_by(class_name=class_name, day=day, time_duration=time_duration).first()

        if existing_class:
            flash('A class with the same name, day, and time already exists.', 'error')
            return redirect(url_for('update_class', class_id=class_id))

        # Delete associated bookings for the class being updated
        try:
            bookings_to_delete = Booking.query.filter_by(class_id=class_id).all()
            for booking in bookings_to_delete:
                db.session.delete(booking)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while deleting associated bookings.', 'error')

        # Update the Class instance
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


@app.route('/delete-class/<int:class_id>', methods=['POST'])
def delete_class(class_id):
    if 'user_id' not in session or session.get('user_role') != 'admin':
        flash('You do not have permission to access this page.', 'error')
        return redirect(url_for('login'))

    class_to_delete = Class.query.get(class_id)
    if class_to_delete:
        db.session.delete(class_to_delete)
        try:
            db.session.commit()
            flash('Class has been deleted successfully!', 'success')
        except Exception as e:
            db.session.rollback()  # Roll back the changes if something goes wrong
            flash('An error occurred while deleting the class.', 'error')
    else:
        flash('Class doesn\'t exist', 'error')

    return redirect(url_for('booking'))


@app.route('/book-class/<int:class_id>', methods=['POST'])
def book_class(class_id):
    if 'user_id' not in session:
        flash('You need to log in to book a class.', 'error')
        return redirect(url_for('login'))

    # Retrieve the logged-in user
    user = User.query.get(session['user_id'])

    # Check if the class exists
    class_to_book = Class.query.get(class_id)
    if not class_to_book:
        flash('Class not found.', 'error')
        return redirect(url_for('booking'))

    # Check if the user is already booked for this class
    existing_booking = Booking.query.filter_by(user_id=user.id, class_id=class_id).first()
    if existing_booking:
        flash('You have already booked this class.', 'info')
        return redirect(url_for('booking'))

    # Retrieve the class name
    class_name = class_to_book.class_name
    day = class_to_book.day
    time_duration = class_to_book.time_duration

    # Create a new booking
    new_booking = Booking(user_id=user.id, class_id=class_id, user_email=user.user_email, class_name=class_name,
                          day=day, time_duration=time_duration)

    try:
        db.session.add(new_booking)
        db.session.commit()
        flash('Class booked successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while booking the class.', 'error')

    return redirect(url_for('booking'))


@app.route('/delete-book/<int:class_id>', methods=['POST'])
def delete_book(class_id):
    if 'user_id' not in session:
        flash('You need to log in to book a class.', 'error')
        return redirect(url_for('login'))

    # Retrieve the logged-in user
    user = User.query.get(session['user_id'])

    # Check if the class exists
    class_to_book = Class.query.get(class_id)
    if not class_to_book:
        flash('Class not found.', 'error')
        return redirect(url_for('booking'))

    # Check if the user is already booked for this class
    existing_booking = Booking.query.filter_by(user_id=user.id, class_id=class_id).first()
    if existing_booking:
        db.session.delete(existing_booking)
        db.session.commit()
        flash('Booking successfully cancelled!', 'info')
        return redirect(url_for('booking'))
    else:
        db.session.rollback()
        flash('Booking not found for the logged-in user and class.', 'error')
        return redirect(url_for('booking'))


if __name__ == '__main__':
    app.run(debug=True)
