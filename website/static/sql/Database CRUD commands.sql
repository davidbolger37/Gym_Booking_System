-----------------------------COMMANDS-----------------------------

-------------------------USEFULL_COMMANDS-------------------------
SHOW DATABASES; = list all databases available
SHOW TABLES; = list all tables
ctrl c = exit --or type exit
DROP DATABASE test_db; = deletes a database and its content
DROP TABLE test_table; = deletes a table from a database

-----------------------------CREATE-----------------------------

INSERT INTO users (first_name, last_name, user_email, user_password, role)
VALUES ('John', 'Doe', 'john@example.com', 'password123', 'user');

INSERT INTO users (first_name, last_name, user_email, user_password, role)
VALUES ('Philip', 'Darcy', 'philip@example.com', 'password456', 'admin');

INSERT INTO class (class_name, day, time_duration)
VALUES ('Yoga', 'Monday', '10:00 AM - 11:00 AM');

INSERT INTO class (class_name, day, time_duration)
VALUES ('Spin', 'Friday', '12:00 AM - 15:00 PM');

INSERT INTO booking (user_id, class_id, user_email, class_name, day, time_duration, booking_at)
(user_id, class_id, 'alice@example.com', 'Pilates', 'Friday', '9:00 AM - 10:00 AM', NOW());


-----------------------------READ-----------------------------

SELECT * FROM users;
SELECT first_name FROM users;
SELECT last_name FROM users;
SELECT user_password FROM users;
SELECT user_email FROM users;
SELECT role FROM users;

SELECT * FROM class;
SELECT class_name FROM class;
SELECT day FROM class;
SELECT time_duration FROM class;

SELECT * FROM booking;
SELECT user_id FROM booking;
SELECT class_id FROM booking;
SELECT booking_at FROM booking;
SELECT user_email FROM booking;
SELECT class_name FROM booking;
SELECT day FROM booking;
SELECT time_duration FROM booking;


-----------------------------UPDATE-----------------------------

UPDATE users
SET first_name = 'Johnny',
    user_email = 'johnny@example.com'
WHERE first_name = 'John';

UPDATE users
SET first_name = 'John',
    user_email = 'john@example.com'
WHERE id = 2;

UPDATE class
SET class_name = 'Pilates',
    time_duration = '11:00 AM - 12:00 PM'
WHERE id = 1;

UPDATE class
SET class_name = 'Pilates',
    time_duration = '11:00 AM - 12:00 PM'
WHERE class = 'Yoga';


-----------------------------DELETE-----------------------------

DELETE FROM users WHERE id = 1;
DELETE FROM users WHERE first_name = 'John';
DELETE FROM users WHERE last_name = 'Doe';
DELETE FROM users WHERE user_email = 'john@example.com';
DELETE FROM users WHERE user_password = 'password123';
DELETE FROM users WHERE role = 'user';

DELETE FROM class WHERE id = 1;
DELETE FROM class WHERE class_name = 'Yoga';
DELETE FROM class WHERE day = 'Monday';
DELETE FROM class WHERE time_duration = '10:00 AM - 11:00 AM';

DELETE FROM booking WHERE id = 1;
DELETE FROM booking WHERE user_id = 1;
DELETE FROM booking WHERE class_id = 1;
DELETE FROM booking WHERE user_email = 'john@example.com';
DELETE FROM booking WHERE class_name = 'Yoga';
DELETE FROM booking WHERE day = 'Monday';
DELETE FROM booking WHERE time_duration = '10:00 AM - 11:00 AM';