
-- 1) Drop (if exists) and create database
DROP DATABASE IF EXISTS complaint_system;
CREATE DATABASE complaint_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE complaint_system;

-- 2) USERS table (admins, employees, citizens)
CREATE TABLE users (
    user_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    phone VARCHAR(24),
    password_hash VARCHAR(255) NOT NULL, -- store bcrypt hash (recommended)
    role VARCHAR(32) NOT NULL DEFAULT 'citizen', -- e.g. 'admin', 'employee', 'citizen'
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- 3) CATEGORIES table (complaint types)
CREATE TABLE categories (
    category_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- 4) COMPLAINTS table (main records)
CREATE TABLE complaints (
    complaint_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNSIGNED NOT NULL,               -- who filed the complaint
    category_id INT UNSIGNED,                    -- nullable: category optional
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'Pending',  -- 'Pending', 'In Progress', 'Resolved', 'Rejected', etc.
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL DEFAULT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB;

-- 5) COMPLAINT HISTORY table (tracks actions/notes on complaints)
CREATE TABLE complaint_history (
    history_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    complaint_id INT UNSIGNED NOT NULL,
    action_taken TEXT NOT NULL,       -- description of what was done/said
    changed_by INT UNSIGNED,          -- user_id of the staff/admin who made the change (nullable)
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (complaint_id) REFERENCES complaints(complaint_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (changed_by) REFERENCES users(user_id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB;

-- 6) Useful indexes
CREATE INDEX idx_complaints_status ON complaints (status);
CREATE INDEX idx_complaints_created_at ON complaints (created_at);
CREATE INDEX idx_users_email ON users (email);

-- 7) Sample seed data (optional)
-- NOTE: Replace the password_hash with a proper bcrypt hash for your password.
-- Example bcrypt hash below corresponds to 'admin123' (you can replace it).
INSERT INTO users (full_name, email, phone, password_hash, role)
VALUES
('System Administrator', 'admin@system.com', '9999999999',
 '$2b$12$1RVqGcQpS8gJxS9hNEAq8eNKqsYzYk6Sj1tUJO5v8L3Q7pSgSM..i',  -- bcrypt for 'admin123' (example)
 'admin');

INSERT INTO categories (name, description)
VALUES
('Water Supply', 'Issues related to water connection, leakage, shortage.'),
('Electricity', 'Power outages, wiring, meter problems.'),
('Roads & Pavement', 'Potholes, damaged roads, street maintenance.'),
('Sanitation', 'Garbage collection, drainage, cleanliness.');

-- 8) Example complaint (optional)
INSERT INTO complaints (user_id, category_id, title, description, status)
VALUES
(1, 1, 'Water leakage near main junction', 'There is continuous leakage from the main valve near 3rd cross. Needs urgent repair.', 'Pending');

-- 9) Example history entry (optional)
INSERT INTO complaint_history (complaint_id, action_taken, changed_by)
VALUES
(1, 'Complaint created by user; initial triage pending.', 1);

USE complaint_system;
UPDATE users
SET password_hash = '123456'
WHERE email = 'admin@system.com';

-- End of script
