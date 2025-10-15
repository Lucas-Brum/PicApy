![Logo](img/logo.jpg)
# User CRUD API with Flask

## 🚀 Project Overview

**PicApy** is a RESTful API developed in Python using the **Flask** framework to meet the requirements of a technical challenge. The main goal is to provide a complete set of **CRUD** (Create, Read, Update, Delete) operations for the `User` entity, with data persistence in a **SQLite** database.

The project is structured following the **Model-View-Controller (MVC)** architectural pattern, ensuring a clear separation of concerns, clean code, and ease of maintenance.

### ✨ Key Features

*   **Framework:** Flask.
*   **Persistence:** SQLite (`database.db` file automatically generated).
*   **Architecture:** MVC Pattern.
*   **Security:** User passwords stored with secure *hash*.
*   **Quality:** Implementation of unit tests with `pytest` and `pytest-flask`.
*   **Validation:** Robust validation of input data (username, email, and password).

## 🛠️ Technologies Used

The project was developed and tested using the following Python version and the libraries listed in `requirements.txt`:

| Technology            | Version | Purpose                                                  |
| :-------------------- | :------ | :------------------------------------------------------- |
| **Python**            | 3.11.9  | Main programming language.                               |
| **Flask**             | 3.1.2   | Web framework for building the API.                      |
| **Werkzeug**          | 3.1.3   | WSGI utility library used by Flask.                      |
| **Pydantic**          | 2.12.2  | Data validation and settings management.                 |
| **email-validator**   | 2.3.0   | Validates email addresses.                               |
| **bcrypt**            | 5.0.0   | Password hashing.                                        |
| **pytest**            | 8.4.2   | Testing framework.                                       |
| **pytest-flask**      | 1.3.0   | Flask extension for testing.                             |
| **black**             | 25.9.0  | Code formatter for Python.                               |
| **click**             | 8.3.0   | Command line interface creation library (used by Flask). |
| **dnspython**         | 2.8.0   | Required dependency for some email validations.          |
| **blinker**           | 1.9.0   | Used for Flask signals/events.                           |
| **typing-extensions** | 4.15.0  | Backports of typing features.                            |
| **typing-inspection** | 0.4.2   | Helper for inspecting types in Python.                   |
| **packaging**         | 25.0    | Library for version and dependency parsing.              |





## ⚙️ Setup and Installation

Follow the steps below to set up and run the project in your local environment.

### 1. Clone the Repository

```bash
git clone https://github.com/Lucas-Brum/PicApy.git
cd PicApy
```

### 2. Create and Activate the Virtual Environment

It is highly recommended to use a virtual environment to isolate project dependencies.

**Linux/macOS:**
```bash
python3.11 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install Dependencies

With the virtual environment activated, install the necessary libraries:

```bash
pip install -r requirements.txt
```

### 4. Run the Application

Execute the main application file:

```bash
python app.py
```

The API will be running at `http://127.0.0.1:5000/` (or the default Flask port).

## 🧪 Running Tests

The project includes unit tests to ensure the correct functioning of the endpoints and validation logic.

### 1. Execute Tests

Make sure the virtual environment is activated and run `pytest` in the project root:

```bash
pytest
```

If you what se more information about the tests use:

```bash
pytest -v
```

### 2. Database Note

The tests use a temporary and isolated SQLite database for each execution, ensuring that the tests are independent and do not interfere with the main application data.

## 🗺️ API Endpoints

The API exposes the following endpoints for managing the `User` entity. All routes use the `/users` prefix.

| Method | Endpoint | Description | Request Body (JSON) | Success Response |
| :--- | :--- | :--- | :--- | :--- |
| **POST** | `/users` | Creates a new user. | `{"user_name": "...", "email": "...", "password": "..."}` | `201 Created` |
| **GET** | `/users` | Returns a list of all users. | N/A | `200 OK` |
| **GET** | `/users/{id}` | Returns the details of a specific user. | N/A | `200 OK` |
| **PUT** | `/users/{id}` | Updates an existing user's data. | `{"user_name": "...", "email": "...", "password": "..."}` (Optional fields) | `200 OK` |
| **DELETE** | `/users/{id}` | Removes a user. | N/A | `200 OK` |

### Usage Example (cURL)

**1. Create User (POST)**

```bash
curl -X POST http://127.0.0.1:5000/users \
-H "Content-Type: application/json" \
-d '{"user_name": "LucasBrum", "email": "lucas.brum@example.com", "password": "SecurePassword123"}'
```

**2. List All Users (GET)**

```bash
curl -X GET http://127.0.0.1:5000/users
```

**3. Get User by ID (GET)**

(Assuming the created user's ID is 1)
```bash
curl -X GET http://127.0.0.1:5000/users/1
```

## 📐 Project Structure

The project follows the MVC pattern, with the following directory organization:

```
PicApy/
├── controller/                 # Business Logic (Controllers)
│   └── user_controller.py      # Manages User CRUD operations
├── model/                      # Data Logic (Models)
│   ├── api/                    # API Helpers
│   │   └── api_utils.py        # API Response Standardization
│   ├── security/               # Security Module
│   │   └── security.py         # Password Hashing and Verification
│   ├── utils/                  # Utilities
│   │   └── validations.py      # Data Validation Logic
│   ├── data_base.py            # Manages SQLite connection and operations
│   ├── user_model.py           # Pydantic User Schema
│   └── user.py                 # User Entity Class (Object-Oriented)
├── test/                       # Unit Tests
│   ├── conftest.py             # Pytest Configurations ('client' fixture)
│   └── test_api.py             # API Endpoint Tests
├── view/                       # Routes (Views)
│   └── users_routes.py         # Flask Endpoint Definition
├── db/                         # Database Folder
│   └── picapy.db               # SQLite Database
├── img/                        # Images
│   └── logo.jpg
├── app.py                      # Application Entry Point
├── factory.py                  # App Factory (if using app factory pattern)
├── requirements.txt            # Project Dependencies
└── README.md                   # This file

```

## 🤝 Contribution

Contributions are welcome! Feel free to open *issues* or submit *pull requests* for improvements, bug fixes, or new features.

## 📄 License

This project is licensed under the [GPL-3.0 License](LICENSE).

