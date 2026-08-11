# Multifactor Biometric Authentication

A Flask-based web application that combines username/password authentication with face biometric verification. The project is designed for secure access control and document permission management in a company environment.

## Overview

This application allows users to:
- register an account with a username and password
- upload a face image for biometric registration
- log in using both credentials and a live/captured face image
- access documents based on assigned permissions
- view admin-only controls for managing users and access rights

The system uses face embedding extraction and similarity matching with `InsightFace` and OpenCV to verify the user’s identity.

## Features

- Multi-factor authentication using password + face verification
- Secure user registration and login flow
- Face embedding extraction using `InsightFace`
- Admin approval and management dashboard
- Document access control with permission-based visibility
- Company landing page and employee portal interface
- SQLite database backend using Flask SQLAlchemy

## Tech Stack

- Python 3.10+
- Flask
- Flask-SQLAlchemy
- OpenCV (`cv2`)
- InsightFace
- NumPy
- HTML / CSS / JavaScript templates
- SQLite

## Project Structure

```text
face_phrase_auth/
├── app.py
├── config.py
├── check_requirements.py
├── README.md
├── requirements.txt
├── models/
│   ├── user.py
│   ├── document.py
│   ├── document_permission.py
│   └── login_log.py
├── routes/
│   ├── __init__.py
│   ├── auth_routes.py
│   ├── admin_routes.py
│   └── dashboard_routes.py
├── services/
│   ├── auth_service.py
│   ├── database.py
│   ├── face_service.py
│   └── __init__.py
├── static/
│   ├── css/
│   ├── js/
│   ├── models/
│   └── haarcascade_frontalface_default.xml
├── templates/
│   ├── admin.html
│   ├── company_home.html
│   ├── dashboard.html
│   ├── document_view.html
│   ├── documents.html
│   ├── login.html
│   ├── manage_documents.html
│   ├── profile.html
│   └── register.html
├── uploads/
│   ├── faces/
│   └── tests/
├── instance/
└── venv/
```

## Setup Instructions

1. Clone the repository
   ```bash
   git clone https://github.com/RealPanzy/Multifactor-Biometric-Authentication.git
   cd Multifactor-Biometric-Authentication
   ```

2. Create and activate a virtual environment
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application
   ```bash
   python app.py
   ```

5. Open the app in the browser
   ```text
   http://127.0.0.1:5000/
   ```

## Default Admin Account

The app creates a default admin user automatically when it starts for the first time:

- Username: `Phase`
- Password: `phaseadmin`

For production use, change the default credentials and secret key.

## Security Notes

- Do not commit sensitive images or personal biometric data to GitHub.
- Keep the `SECRET_KEY` private.
- Do not use the default admin credentials in a live deployment.
- Add generated files like `__pycache__`, uploaded images, and local databases to `.gitignore`.

## Usage Flow

1. Open the app homepage.
2. Register a new user with a username, password, and face image.
3. Log in using the credentials and a biometric image.
4. Access authorized documents based on admin-granted permissions.
5. Use the admin panel to approve users and manage document access.

## License

This project is for educational and demonstration purposes.

## Author

Developed as a multifactor biometric authentication prototype for secure access and document authorization.