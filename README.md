# DreamHomes - Real Estate Platform

A full-featured real estate platform built with FastAPI and vanilla JavaScript. Users can browse properties, save favorites, post listings, schedule viewings, and communicate with property owners.

## Features

- **User Authentication**: Secure JWT-based authentication with bcrypt password hashing
- **Property Listings**: Post, browse, search, and filter properties
- **Favorites**: Save properties to your favorites list
- **Reviews**: Rate and review properties
- **Inquiries**: Send messages to property owners
- **Appointments**: Schedule property viewings
- **Admin Panel**: Manage users and properties
- **Email Notifications**: Automated emails for key actions (welcome, inquiries, appointments)
- **File Uploads**: Upload property images and user avatars

## Tech Stack

**Backend:**
- FastAPI (Python web framework)
- SQLAlchemy (ORM)
- PostgreSQL (Database)
- JWT (Authentication)
- Python-dotenv (Environment variables)

**Frontend:**
- Vanilla JavaScript
- HTML5/CSS3
- Responsive design

## Prerequisites

- Python 3.8+
- PostgreSQL 12+
- pip (Python package manager)

## Installation

### 1. Clone the repository

```bash
cd /path/to/project
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Copy the example environment file and configure it:

```bash
cp .env.example .env
```

Edit `.env` with your actual configuration:

```env
# Database
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/dreamhomes

# JWT Secret (generate with: openssl rand -hex 32)
SECRET_KEY=your-generated-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=1440

# Email (optional - leave EMAIL_USER empty to disable)
EMAIL_HOST=sandbox.smtp.mailtrap.io
EMAIL_PORT=2525
EMAIL_USER=your_mailtrap_username
EMAIL_PASSWORD=your_mailtrap_password
EMAIL_FROM=DreamHomes <noreply@dreamhomes.com>
```

**Important:** Generate a secure SECRET_KEY:
```bash
openssl rand -hex 32
```

### 5. Set up the database

Create the PostgreSQL database:

```bash
psql -U postgres
CREATE DATABASE dreamhomes;
\q
```

The application will automatically create tables on first run using SQLAlchemy models.

Alternatively, you can use the SQL schema:

```bash
psql -U postgres -d dreamhomes -f database_schema.sql
```

### 6. Create an admin user (optional)

```bash
python make_admin.py
```

Follow the prompts to create an admin account.

## Running the Application

### Option 1: Docker (Recommended)

The easiest way to run the application with all dependencies:

```bash
# Start the application and database
docker-compose up -d

# View logs
docker-compose logs -f web

# Stop the application
docker-compose down

# Stop and remove volumes (clears database)
docker-compose down -v
```

The application will be available at:
- **Frontend**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc

To configure environment variables with Docker, create a `.env` file in the project root or modify the environment section in `docker-compose.yml`.

### Option 2: Local Development Server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The application will be available at:
- **Frontend**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc

### Option 3: Production Server

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Project Structure

```
realestate/
├── routers/              # API route handlers
│   ├── auth.py           # Authentication endpoints
│   ├── properties.py     # Property CRUD operations
│   ├── favorites.py      # Favorites management
│   ├── reviews.py        # Property reviews
│   ├── inquiries.py      # Buyer-seller communication
│   ├── appointments.py   # Property viewing appointments
│   ├── users.py          # User profile management
│   └── admin.py          # Admin panel endpoints
├── frontend/             # HTML/CSS/JS frontend
│   ├── home.html         # Landing page
│   ├── login.html        # Login page
│   ├── signup.html       # Registration page
│   ├── property.html     # Property details
│   ├── profile.html      # User profile
│   ├── favorites.html    # User favorites
│   ├── seller.html       # Seller dashboard
│   ├── inquiries.html    # Inquiry management
│   ├── appointments.html # Appointment management
│   ├── admin.html        # Admin panel
│   └── css.css           # Styles
├── utils/                # Utility modules
│   └── email.py          # Email sending functions
├── uploads/              # User-uploaded files
│   ├── images/           # Property images
│   └── avatars/          # User avatars
├── main.py               # Application entry point
├── models.py             # Database models
├── schemas.py            # Pydantic schemas
├── database.py           # Database configuration
├── auth.py               # Authentication utilities
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variable template
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## API Endpoints

### Authentication
- `POST /auth/signup` - Register new user
- `POST /auth/login` - Login and get JWT token

### Properties
- `GET /properties` - List all properties (with filters)
- `GET /properties/{id}` - Get property details
- `POST /properties` - Create new property (authenticated)
- `POST /properties/{id}/image` - Upload property image
- `DELETE /properties/{id}` - Delete property (owner/admin only)

### Favorites
- `POST /favorites/{property_id}` - Add to favorites
- `DELETE /favorites/{property_id}` - Remove from favorites
- `GET /favorites` - Get user's favorites

### Reviews
- `POST /reviews/{property_id}` - Add review
- `GET /reviews/{property_id}` - Get property reviews
- `DELETE /reviews/{review_id}` - Delete review

### Inquiries
- `POST /inquiries/{property_id}` - Send inquiry
- `GET /inquiries/mine` - Get sent inquiries
- `GET /inquiries/received` - Get received inquiries
- `PUT /inquiries/{id}/reply` - Reply to inquiry

### Appointments
- `POST /appointments/{property_id}` - Book appointment
- `GET /appointments/mine` - Get my appointments
- `GET /appointments/received` - Get received appointments
- `PUT /appointments/{id}/confirm` - Confirm appointment
- `PUT /appointments/{id}/cancel` - Cancel appointment

### Users
- `GET /users/me` - Get current user profile
- `PUT /users/profile` - Update profile
- `POST /users/avatar` - Upload avatar
- `PUT /users/password` - Change password

### Admin
- `GET /admin/users` - List all users
- `DELETE /admin/users/{id}` - Delete user
- `PUT /admin/users/{id}/toggle-admin` - Toggle admin status
- `GET /admin/properties` - List all properties
- `DELETE /admin/properties/{id}` - Delete property

## Email Configuration

### Development (Mailtrap)

Sign up at [Mailtrap](https://mailtrap.io/) and use the provided SMTP credentials in your `.env` file.

### Production (Gmail)

1. Enable 2-Factor Authentication on your Gmail account
2. Generate an App Password: https://myaccount.google.com/apppasswords
3. Update `.env`:

```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
```

### Disable Emails

To disable email functionality, leave `EMAIL_USER` empty in `.env`:

```env
EMAIL_USER=
```

## Security Notes

- Never commit `.env` file to version control
- Use strong, randomly generated SECRET_KEY in production
- Change default database credentials
- Consider using environment-specific CORS origins in production
- Regularly update dependencies for security patches

## Troubleshooting

### Database connection errors
- Ensure PostgreSQL is running
- Verify DATABASE_URL in `.env` matches your PostgreSQL configuration
- Check that the database exists

### Email not sending
- Verify EMAIL_USER and EMAIL_PASSWORD are correct
- Check email service is not blocking connections
- Review application logs for specific error messages

### Import errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Activate virtual environment before running

## License

This project is for educational purposes.

## Contributing

Feel free to submit issues and pull requests for improvements.
