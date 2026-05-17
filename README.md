# OTP SaaS Backend

A scalable, API-first One-Time Password (OTP) generation and verification service. This project provides developers with an easy-to-use API to send and verify OTPs via email, along with a full-stack dashboard to manage API keys and customize email templates.

## 🚀 Features

- **Developer Dashboard**: Register, login, and manage your API keys and service settings.
! [demo screenshot](screenshots/Screenshot%202026-05-18%20013553.png)
! [demo screenshot](screenshots/Screenshot%202026-05-18%20013625.png)
- **API Key Authentication**: Secure all API endpoints using a randomly generated `x-api-key`.
! [demo screenshot](screenshots/Screenshot%202026-05-18%20013750.png)
- **Customizable Emails**: Modify the organization name, email subject, support email, and footer text sent to your end users.
! [demo screenshot](screenshots/Screenshot%202026-05-18%20013809.png)
- **OTP Generation & Delivery**: Generates a secure 6-digit OTP and sends it reliably via SMTP (Gmail).
- **OTP Verification**: Simple API endpoint to verify if the provided OTP is correct.
- **Security**: Argon2 password hashing for user accounts and secure OTP handling.

## 🛠️ Technology Stack

- **Backend Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Database ORM**: [SQLAlchemy](https://www.sqlalchemy.org/)
- **Authentication/Security**: Passlib (Argon2)
- **Frontend**: Jinja2 Templates, HTML/CSS (Static)
- **Email Delivery**: `smtplib` (SMTP integration)

## 📁 Project Structure

```
otp/
├── app.py             # Main FastAPI application and route definitions
├── database.py        # Database configuration and session management
├── models.py          # SQLAlchemy database models
├── verify.py          # Verification utilities
├── .env.example       # Example environment variables file
└── frontend/          # Full-stack frontend assets
    ├── static/        # CSS, JS, Images
    └── templates/     # Jinja2 HTML Templates
```

## ⚙️ Getting Started

### Prerequisites

- Python 3.8+
- An SMTP server (e.g., Gmail App Password)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/otp_saas_backend.git
   cd otp_saas_backend
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install the dependencies:**
   ```bash
   pip install fastapi uvicorn sqlalchemy passlib argon2-cffi python-dotenv python-multipart jinja2
   ```

4. **Environment Variables:**
   Create a `.env` file in the root directory based on `.env.example`:
   ```env
   EMAIL_USER=your-email@gmail.com
   EMAIL_PASS=your-app-password
   ```

### Running the Application

Run the FastAPI development server using Uvicorn:

```bash
uvicorn app:app --reload
```

The application will be accessible at `http://127.0.0.1:8000`.

## 📖 API Documentation

### `POST /send-otp`

Generates and sends a 6-digit OTP to the specified email.

**Headers:**
- `x-api-key`: Your secret API key obtained from the dashboard.

**Request Body (JSON):**
```json
{
  "email": "user@example.com"
}
```

**Response:**
```json
{
  "success": true,
  "message": "otp generated successfully"
}
```

### `POST /verify`

Verifies the provided OTP for the given email.

**Headers:**
- `x-api-key`: Your secret API key.

**Request Body (JSON):**
```json
{
  "email": "user@example.com",
  "otp": "123456"
}
```

**Response (Success):**
```json
{
  "success": true,
  "message": "otp verified"
}
```

## 🎨 Dashboard Usage

1. Navigate to `http://127.0.0.1:8000/register` to create a developer account.
2. Log in at `http://127.0.0.1:8000/login`.
3. In the **Dashboard**, you can copy your unique `API Key`.
4. Head to **Settings** to customize the appearance and content of the OTP emails sent to your users.

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
