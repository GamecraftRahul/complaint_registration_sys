# Complaint Registration System

A simple Complaint Registration System built using **Python**, **Tkinter GUI**, and **MySQL**. The application allows citizens to register, log in, submit complaints, and track complaint status, while administrators can view and update complaint statuses through a dedicated dashboard.

---

## Features

### User Features

* User Registration
* User Login Authentication
* Submit Complaints
* Select Complaint Categories
* View Complaint Submission Confirmation

### Admin Features

* Admin Login
* View All Complaints
* Update Complaint Status
* Complaint Management Dashboard

### Complaint Status Options

* Pending
* In Progress
* Resolved
* Rejected

---

## Technologies Used

| Technology             | Purpose               |
| ---------------------- | --------------------- |
| Python                 | Backend Logic         |
| Tkinter                | GUI Development       |
| MySQL                  | Database Management   |
| mysql-connector-python | Database Connectivity |

---

## Project Structure

```text
Complaint Registration System
│
├── complaint_register_sys_code.py
├── MySQL Database
│   ├── users
│   ├── complaints
│   └── categories
└── README.md
```

---

## Database Configuration

Update the database credentials inside the project file if needed:

```python
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="YOUR_PASSWORD",
        database="complaint_system"
    )
```

---

## Required Database

Create a MySQL database named:

```sql
CREATE DATABASE complaint_system;
```

Use the database:

```sql
USE complaint_system;
```

---

## Create Users Table

```sql
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    password_hash VARCHAR(255),
    role ENUM('admin','citizen') DEFAULT 'citizen'
);
```

---

## Create Categories Table

```sql
CREATE TABLE categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100)
);
```

---

## Create Complaints Table

```sql
CREATE TABLE complaints (
    complaint_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    category_id INT,
    title VARCHAR(255),
    description TEXT,
    status VARCHAR(50) DEFAULT 'Pending',
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);
```

---

## Sample Categories

```sql
INSERT INTO categories (name) VALUES
('Road Issues'),
('Water Supply'),
('Electricity'),
('Garbage Collection'),
('Public Safety');
```

---

## Create Admin Account

```sql
INSERT INTO users
(full_name,email,phone,password_hash,role)
VALUES
(
'Administrator',
'admin@complaint.com',
'9999999999',
'admin123',
'admin'
);
```

---

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/your-username/complaint-registration-system.git
cd complaint-registration-system
```

### 2. Install Dependencies

```bash
pip install mysql-connector-python
```

### 3. Configure MySQL

* Create database
* Create tables
* Insert categories
* Create admin account

### 4. Run Application

```bash
python complaint_register_sys_code.py
```

---

## Application Workflow

### Citizen

1. Open Application
2. Register New Account
3. Login
4. Select Complaint Category
5. Enter Complaint Details
6. Submit Complaint

### Administrator

1. Login Using Admin Credentials
2. Open Admin Dashboard
3. View All Complaints
4. Select Complaint
5. Update Complaint Status

---

## Screens Included

* Login Window
* Registration Window
* Complaint Submission Form
* Admin Dashboard
* Status Update Window

---

## Future Improvements

* Password Hashing & Security
* Email Notifications
* Complaint Tracking History
* Search and Filter Complaints
* File/Image Upload Support
* User Complaint History
* Dashboard Analytics
* Multi-Level Admin Roles
* Complaint Priority Levels

---

## Security Note

This project is developed for educational purposes. Passwords are currently stored in plain text. For production use:

* Use password hashing (bcrypt)
* Add input validation
* Implement session management
* Use environment variables for database credentials
* Enable role-based access control

---

## Author

Developed as a Python Tkinter and MySQL Complaint Management System project for learning database connectivity, GUI development, and CRUD operations.

---

## License

This project is open-source and available for educational and personal use.
