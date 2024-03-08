-----------------------------COMMANDS-----------------------------

-------------------------USEFULL_COMMANDS-------------------------
SHOW DATABSES; = list all databases available
SHOW TABLES; = list all tables
ctrl c = exit
DROP DATABASE test_db; = deletes a databse and its content
DROP TABLE test_table; = deletes a table from a database

-----------------------------CREATE-----------------------------

INSERT INTO users (first_name, last_name, email, password, role)
VALUES ('John', 'Doe', 'john@example.com', 'password123', 'user');

INSERT INTO users (first_name, last_name, email, password, role)
VALUES ('Philip', 'Darcy', 'philip@example.com', 'password456', 'admin');

INSERT INTO class (class, day, time_duration)
VALUES ('Yoga', 'Monday', '10:00 AM - 11:00 AM');

INSERT INTO class (class, day, time_duration)
VALUES ('Spin', 'Friday', '12:00 AM - 1:00 PM');

INSERT INTO booking (user_id, class_id, booking_at)
VALUES (1, 1, NOW());

INSERT INTO booking (user_id, class_id, booking_at)
VALUES (
    (SELECT id FROM users WHERE first_name = 'Jane' LIMIT 1),
    (SELECT id FROM class WHERE class = 'Yoga' LIMIT 1),
    NOW()
);

-----------------------------READ-----------------------------

SELECT * FROM users;
SELECT first_name FROM users;
SELECT last_name FROM users;
SELECT password FROM users;
SELECT email FROM users;
SELECT role FROM users;

SELECT * FROM class;
SELECT class FROM class;
SELECT day FROM class;
SELECT time_duration FROM class;

SELECT * FROM booking;
SELECT user_id FROM booking;
SELECT class_id FROM booking;
SELECT booking_at FROM booking;


-----------------------------UPDATE-----------------------------

UPDATE users
SET first_name = 'Johnny',
    email = 'johnny@example.com'
WHERE first_name = 'John';

UPDATE users
SET first_name = 'John',
    email = 'john@example.com'
WHERE id = 2;

UPDATE class
SET class = 'Pilates',
    time_duration = '11:00 AM - 12:00 PM'
WHERE id = 1;

UPDATE class
SET class = 'Pilates',
    time_duration = '11:00 AM - 12:00 PM'
WHERE class = 'Yoga';

-----------------------------DELETE-----------------------------

DELETE FROM users WHERE id = 1;
DELETE FROM users WHERE first_name = 'John';
DELETE FROM users WHERE last_name = 'Doe';
DELETE FROM users WHERE email = 'john@example.com';
DELETE FROM users WHERE password = 'password123';
DELETE FROM users WHERE role = 'user';

DELETE FROM class WHERE id = 1;
DELETE FROM class WHERE class = 'Yoga';
DELETE FROM class WHERE day = 'Monday';
DELETE FROM class WHERE time_duration = '10:00 AM - 11:00 AM';

DELETE FROM booking WHERE id = 1;