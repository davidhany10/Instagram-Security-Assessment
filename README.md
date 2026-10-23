 
# 📸 Instagram Clone — Flask & MySQL

<p align="center">
  <img src="docs/images/banner.png" alt="Instagram Clone Project Banner" width="100%">
</p>

<p align="center">
  A Python-powered social media web application inspired by Instagram.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-Web%20Framework-black?logo=flask" alt="Flask">
  <img src="https://img.shields.io/badge/MySQL-Database-4479A1?logo=mysql&logoColor=white" alt="MySQL">
  <img src="https://img.shields.io/badge/Testing-Pytest-0A9EDC?logo=pytest&logoColor=white" alt="Pytest">
  <img src="https://img.shields.io/badge/Load%20Testing-Locust-00A86B" alt="Locust">
</p>

---

## 📖 Overview

Instagram Clone is a web-based social media application built with **Python, Flask, and MySQL**. It demonstrates core social networking workflows, including user registration, authentication, posts, likes, and comments.

The project also includes automated application tests, database operation checks, password-hashing verification, and a Locust script for exercising selected user workflows under simulated traffic.

It is intended for learning, experimentation, and demonstrating web development and software testing concepts.

## ✨ Features

- **User Registration:** Create an account using a username, email, and password.
- **User Login:** Authenticate users using stored password hashes.
- **Session Management:** Maintain login state and support logout.
- **Post Feed:** Retrieve posts and display associated user information.
- **Likes:** Add or remove a like on a post.
- **Comments:** Submit comments associated with posts and users.
- **MySQL Integration:** Store and retrieve application data.
- **CSRF Protection:** Integrate Flask-WTF CSRF protection.
- **Automated Testing:** Test registration, login, likes, comments, and database operations.
- **Load Testing:** Use Locust to simulate selected registration, login, like, comment, and logout requests.

*The implemented functionality is based on the supplied source files; additional Instagram features may require further development.*

## 🧰 Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Flask | Web application and routing |
| MySQL | Persistent data storage |
| Werkzeug | Password hashing and verification |
| Flask-WTF | CSRF protection |
| Pytest | Automated application tests |
| Locust | Simulated user traffic |
| HTML, CSS, JavaScript | Web interface |

## 🧪 Testing & Quality Assurance

Testing is an important part of this project. The supplied files cover several application workflows and database operations.

### 1. Application Testing — `test_app.py`

The test suite uses Flask's test client to exercise application routes.

| Test | What it checks |
|---|---|
| `test_register_user` | Registers a user and checks that the account exists with a verifiable password hash. |
| `test_login_success` | Checks the login workflow for a test user. |
| `test_comment_post` | Submits a comment and checks that it is stored in the database. |
| `test_like_post` | Submits a like and checks for the corresponding database record. |

### 2. Database Testing — `test_db.py`

The database test script includes checks for the following operations:

- Database connectivity using `SELECT 1`.
- Creating a test user.
- Reading user data.
- Updating a username.
- Deleting a test user.

The script prints status messages for these operations. These checks should be reviewed and run against a dedicated test database before being treated as verified test results.

### 3. Password Verification — `check.py`

The project includes a small utility that uses Werkzeug's `check_password_hash()` function to verify a password against a stored hash.

### 4. Load Testing — `locustfile.py`

The Locust script simulates user activity by attempting to:

1. Register a generated test account.
2. Log in.
3. Submit a like request.
4. Submit a comment.
5. Log out.

Locust can help examine response times, request failures, and behavior under simulated concurrent traffic. No specific load-test performance result is claimed here.

## 📂 Project Structure

```text
full insta page and testing/
│
├── app.py
├── config.py
├── db.py
├── models.py
├── forms.py
├── check.py
├── update_password.py
│
├── test_app.py
├── test_db.py
├── locustfile.py
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── home.html
│   ├── profile.html
│   ├── post.html
│   ├── add_post.html
│   ├── stories.html
│   ├── notifications.html
│   ├── dashboard.html
│   └── change_password.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   └── profile_pics/
│
├── docs/
│   └── images/
│       └── instagram-banner.png
│
└── README.md
```

This is a documentation overview of the supplied archive. Some templates, models, and utility files may require additional review to determine their exact functionality.

## ⚙️ Installation & Setup

### Prerequisites

- Python 3
- MySQL Server
- pip
- A terminal or command prompt

### 1. Clone the Repository

```bash
git clone https://github.com/davidhany10/Instagram-Clone.git
cd Instagram-Clone
```

Replace the repository URL if your GitHub repository uses a different name.

### 2. Create a Virtual Environment

**Windows:**

```cmd
python -m venv .venv
.venv\Scripts\activate
```

**Linux or macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

Install the libraries required by the project:

```bash
pip install Flask Flask-WTF mysql-connector-python python-dotenv pytest locust
```

Review the imports and your environment to ensure all required packages are installed. A `requirements.txt` file is recommended for reproducible installations.

### 4. Configure the Database

The supplied `config.py` reads these environment variables:

```text
DB_HOST
DB_USER
DB_PASSWORD
DB_NAME
SECRET_KEY
```

The default database name is `instagram_clone`. Configure MySQL and create the required tables before running the application.

Use environment variables or a local `.env` file for configuration. Do not commit database passwords or production secrets to GitHub.

### 5. Start the Application

```bash
python app.py
```

Open the local address shown in the terminal, typically:

```text
http://127.0.0.1:5000
```

## ▶️ Running the Tests

### Run the application tests

From the project root:

```bash
pytest -v test_app.py
```

These tests require a working database and the schema expected by the application.

### Run the database operation checks

```bash
python test_db.py
```

This script performs database operations and prints status messages. Use a dedicated test database because it creates, updates, and deletes records.

### Run the password verification utility

```bash
python check.py
```

### Run the Locust load test

Start the Flask application first, then open another terminal and run:

```bash
locust -f locustfile.py --host http://127.0.0.1:5000
```

Open the Locust web interface at:

```text
http://localhost:8089
```

Choose the number of simulated users and the spawn rate before starting the test. Use a test environment with disposable accounts and data.

## 🔐 Security Considerations

The supplied code uses Werkzeug password hashing and integrates CSRF protection. Before deploying the application publicly, consider the following:

- Replace fallback secrets with strong environment-based values.
- Remove default database credentials from configuration.
- Verify authorization for all post, like, and comment operations.
- Validate form inputs and handle database errors safely.
- Avoid exposing raw exception messages or sensitive information.
- Add rate limiting and account-abuse protections.
- Review session cookie settings and HTTPS configuration.
- Run tests against isolated test data rather than production records.

These are recommended hardening measures, not claims that every control is already implemented.

## 🚀 Future Improvements

- Add a complete follow/unfollow workflow.
- Improve profile editing and account settings.
- Expand automated test coverage.
- Add assertions and clear failure reporting to database tests.
- Introduce fixtures for repeatable test data.
- Record Locust response times and failure rates.
- Add CI automation for tests.
- Document database schema and installation requirements.
- Improve input validation and error handling.

## 👨‍💻 Author

**David Hany**

Computer Science & Artificial Intelligence

GitHub: [@davidhany10](https://github.com/davidhany10)

## 📄 License

A license file was not identified in the supplied project archive. Add a `LICENSE` file to specify the terms under which the project may be used and distributed.

---

<p align="center">
  Built with Python, Flask, MySQL, and a focus on testing.
</p>
