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
    user_email VARCHAR(255) NOT NULL,
    class_name VARCHAR(40) NOT NULL,
    day VARCHAR(15) NOT NULL,
    time_duration VARCHAR(40) NOT NULL,
    booking_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (class_id) REFERENCES class(id) ON DELETE CASCADE
);

-- Populate the 'users' table
INSERT INTO users (first_name, last_name, user_email, user_password, role) VALUES
('Jane', 'Smith', 'jane@example.com', 'abc123', 'admin'),
('John', 'Doe', 'john@example.com', 'password123', 'user'),
('Mason', 'Cullen', 'mason@example.com', 'mason_cullen', 'user'),
('Devin', 'Weston', 'devin@example.com', 'westonPOP', 'user'),
('Alice', 'Johnson', 'alice@example.com', 'qwerty', 'user');

-- Populate the 'class' table
INSERT INTO class (class_name, day, time_duration) VALUES
('Yoga', 'Monday', '10:00 AM - 11:00 AM'),
('Swimming', 'Monday', '12:00 AM - 3:00 PM'),
('Weightlifting', 'Tuesday', '3:00 PM - 5:00 PM'),
('Zumba', 'Tuesday', '6:00 PM - 7:00 PM'),
('Pilates', 'Wednesday', '9:00 AM - 10:00 AM'),
('Running', 'Wednesday', '1:00 PM - 2:00 PM'),
('Spinning', 'Thursday', '10:00 AM - 11:00 AM'),
('Cardio', 'Thursday', '4:00 PM - 6:00 PM'),
('Crossfit', 'Friday', '6:00 PM - 7:00 PM'),
('Pilates', 'Friday', '8:00 PM - 10:00 PM'),
('Spinning', 'Saturday', '6:00 AM - 8:00 AM'),
('Cardio', 'Saturday', '9:00 AM - 10:00 AM');

-- Populate the 'booking' table
INSERT INTO booking (user_id, class_id, user_email, class_name, day, time_duration, booking_at) VALUES
(2, 1, 'john@example.com', 'Yoga', 'Monday', '10:00 AM - 11:00 AM', NOW()),
(5, 3, 'alice@example.com', 'Weightlifting', 'Tuesday', '3:00 PM - 5:00 PM', NOW()),
(3, 4, 'mason@example.com', 'Zumba', 'Wednesday', '9:00 AM - 10:00 AM', NOW()),
(5, 7, 'alice@example.com', 'Spinning', 'Thursday', '10:00 AM - 11:00 AM', NOW()),
(4, 9, 'devin@example.com', 'Crossfit', 'Friday', '6:00 PM - 7:00 PM', NOW()),
(3, 12, 'mason@example.com', 'Cardio', 'Saturday', '9:00 AM - 10:00 AM', NOW());