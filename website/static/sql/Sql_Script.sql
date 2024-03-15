CREATE DATABASE IF NOT EXISTS gym_db;
USE Gym_db;

CREATE TABLE IF NOT EXISTS users (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(40) NOT NULL,
    last_name VARCHAR(40) NOT NULL,
    user_email VARCHAR(255) NOT NULL,
    user_password VARCHAR(255) NOT NULL,
    role ENUM('user', 'admin')
);

CREATE TABLE IF NOT EXISTS class (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    class_name VARCHAR(40) NOT NULL,
    day VARCHAR(15) NOT NULL,
    time_duration VARCHAR(40) NOT NULL
);

CREATE TABLE IF NOT EXISTS booking (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    class_id INT NOT NULL,
    booking_at TIMESTAMP,
    user_email VARCHAR(255) NOT NULL,
    class_name VARCHAR(40) NOT NULL,
    day VARCHAR(15) NOT NULL,
    time_duration VARCHAR(40) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (class_id) REFERENCES class(id) ON DELETE CASCADE
);

-- Populate the 'users' table
INSERT INTO users (first_name, last_name, user_email, user_password, role) VALUES
('John', 'Doe', 'john@example.com', 'password123', 'user'),
('Jane', 'Smith', 'jane@example.com', 'abc123', 'admin'),
('Alice', 'Johnson', 'alice@example.com', 'qwerty', 'user');

-- Populate the 'class' table
INSERT INTO class (class_name, day, time_duration) VALUES
('Yoga', 'Monday', '10:00 AM - 11:00 AM'),
('Zumba', 'Tuesday', '6:00 PM - 7:00 PM'),
('Pilates', 'Wednesday', '9:00 AM - 10:00 AM'),
('Yoga', 'Thursday', '10:00 AM - 11:00 AM'),
('Zumba', 'Friday', '6:00 PM - 7:00 PM'),
('Pilates', 'Saturday', '9:00 AM - 10:00 AM'),
('Yoga', 'Thursday', '10:00 AM - 11:00 AM'),
('Zumba', 'Friday', '6:00 PM - 7:00 PM'),
('Pilates', 'Saturday', '9:00 AM - 10:00 AM'),
('Zumba', 'Monday', '12:00 AM - 15:00 AM');

-- Populate the 'booking' table
INSERT INTO booking (user_id, class_id, user_email, class_name, day, time_duration, booking_at) VALUES
(1, 1, 'john@example.com', 'Yoga', 'Monday', '10:00 AM - 11:00 AM', NOW()),
(2, 2, 'jane@example.com', 'Zumba', 'Wednesday', '6:00 PM - 7:00 PM', NOW()),
(3, 3, 'alice@example.com', 'Pilates', 'Friday', '9:00 AM - 10:00 AM', NOW());

