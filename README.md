# Flask Authentication Website

This project is a Flask-based web application that provides user authentication features, including registration, login, and an admin dashboard for user management.

## Features

- User registration and login
- Admin dashboard for managing users
- User management functionalities
- Responsive design with a clean layout

## Project Structure

```
flask-auth-website
├── app.py                # Entry point of the application
├── config.py             # Configuration settings
├── requirements.txt      # Project dependencies
├── static                # Static files (CSS, JS)
│   ├── css
│   │   └── style.css     # Styles for the website
│   └── js
│       └── main.js       # Client-side JavaScript
├── templates             # HTML templates
│   ├── admin
│   │   ├── dashboard.html # Admin dashboard template
│   │   └── users.html    # User management template
│   ├── auth
│   │   ├── login.html    # Login page template
│   │   └── register.html  # Registration page template
│   ├── base.html         # Base template
│   └── index.html        # Homepage template
├── models.py             # Database models
├── forms.py              # Form classes for registration and login
├── routes                # Route definitions
│   ├── __init__.py       # Initializes routes package
│   ├── admin.py          # Admin routes
│   ├── auth.py           # Authentication routes
│   └── main.py           # Main application routes
└── README.md             # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd flask-auth-website
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Configure the application settings in `config.py`.

4. Run the application:
   ```
   python app.py
   ```

## Usage

- Navigate to the homepage to access the registration and login pages.
- Admin users can access the dashboard to manage user accounts.

## License

This project is licensed under the MIT License.