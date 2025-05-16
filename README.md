# Risk Assessment Application with Login System

This is a Flask-based risk assessment application with user authentication.

## Setup Instructions

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Initialize the database:
```bash
python init_db.py
```

3. Run the application:
```bash
python app.py
```

## Sample Account
- Email: admin@example.com
- Password: Admin123!

## Features
- User authentication (login/register)
- Risk assessment questionnaire
- Results tracking
- SQLite database for data persistence

## Project Structure

```
risk-assessment/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
└── templates/         # HTML templates
    ├── base.html     # Base template with common elements
    ├── question.html # Template for displaying questions
    └── results.html  # Template for showing results
```

## Security Note

For production deployment, make sure to:
1. Change the secret key in `app.py`
2. Enable HTTPS
3. Implement proper user session management
4. Add input validation and sanitization
5. Configure proper logging python app.py