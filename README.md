# 🤖 AI Freelancer Assistant

A complete AI-powered web application that helps freelancers automate their daily workflow. Generate proposals, cover letters, gig descriptions, invoices, contracts, and client replies using AI.

![Django](https://img.shields.io/badge/Django-4.2-green)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## ✨ Features

### 🔐 Authentication
- User Registration & Login
- Password Reset via Email
- Session Management
- User Profile with Profile Picture

### 📊 Dashboard
- Overview of all activities
- AI Credits Display
- Quick Actions for all features
- Recent Activities Timeline

### 🤖 AI-Powered Generators
- **Proposal Generator** – Create professional proposals using AI
- **Cover Letter Generator** – Generate tailored cover letters
- **Gig Description Generator** – Create SEO-optimized gig descriptions with FAQs
- **Smart Pricing Calculator** – Get AI-powered pricing suggestions
- **Client Reply Generator** – Generate professional responses to client messages
- **Contract Generator** – Create AI-generated contracts
- **Invoice Generator** – Generate professional invoices with PDF export

### 📁 Document Management
- Full CRUD operations
- Document History with Filtering
- Copy to Clipboard
- PDF Export for Proposals, Contracts, and Invoices

### 🎨 User Experience
- Responsive Design
- Dark & Light Theme Support
- Email Notifications
- Loading Indicators
- Form Validation
- Error Handling

---

## 🛠️ Tech Stack

### Backend
- **Django 4.2.7** – Python Web Framework
- **SQLite** – Development Database
- **PostgreSQL** – Recommended for Production

### Frontend
- **HTML5**
- **CSS3**
- **Bootstrap 5**
- **JavaScript**

### AI Integration
- **Google Gemini API**
- **OpenAI API** *(Optional / Configurable)*

### PDF Generation
- **xhtml2pdf**

### Deployment
- **Gunicorn**
- **WhiteNoise**

---

# 📦 Installation

Follow these steps to set up the project on your local machine.

## Prerequisites

- Python 3.9 or higher
- pip (Python Package Manager)
- Git (Optional)

---

## Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/ai-freelancer-assistant.git
cd ai_freelancer_assistant
```

---

## Step 2: Create a Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Step 4: Set Up Environment Variables

Create a `.env` file in the project root.

### Windows

```bash
type nul > .env
```

### macOS/Linux

```bash
touch .env
```

Add the following variables:

```env
SECRET_KEY=your-secret-key-here
GEMINI_API_KEY=your-google-gemini-api-key
ENV=development
ALLOWED_HOSTS=localhost,127.0.0.1
```

---

## Step 5: Apply Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Step 6: Create an Admin User

```bash
python manage.py createsuperuser
```

---

## Step 7: Run the Development Server

```bash
python manage.py runserver
```

The application will be available at:

```
http://127.0.0.1:8000/
```

---

## 📂 Project Structure

```
ai_freelancer_assistant/
├── ai_freelancer_assistant/
│   ├── __init__.py
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL routing
│   └── wsgi.py              # WSGI configuration
├── accounts/                # Authentication & user profiles
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── proposals/               # Proposal generator
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── coverletters/            # Cover letter generator
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── gigs/                    # Gig description generator
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── pricing/                 # Pricing calculator
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── replies/                 # Client reply generator
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── invoices/                # Invoice generator
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── contracts/               # Contract generator
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── history/                 # Document history
│   ├── views.py
│   └── urls.py
├── utils/
│   └── ai_helper.py         # AI integration functions
├── templates/               # HTML templates
│   ├── base.html           # Base template
│   ├── accounts/           # Auth templates
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── dashboard.html
│   │   ├── profile.html
│   │   ├── profile_edit.html
│   │   ├── change_password.html
│   │   └── settings.html
│   ├── proposals/          # Proposal templates
│   │   ├── create.html
│   │   ├── list.html
│   │   ├── detail.html
│   │   ├── edit.html
│   │   ├── delete.html
│   │   ├── generate.html
│   │   └── pdf_template.html
│   ├── coverletters/       # Cover letter templates
│   ├── gigs/              # Gig description templates
│   ├── pricing/           # Pricing calculator templates
│   ├── replies/           # Client reply templates
│   ├── invoices/          # Invoice templates
│   ├── contracts/         # Contract templates
│   └── history/           # History templates
├── static/                  # Static files (CSS, JS)
│   ├── css/
│   └── js/
├── media/                   # User-uploaded files
│   └── profile_pics/
├── backups/                 # Database backups
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables
├── .gitignore              # Git ignore rules
├── .env.example            # Example environment variables
├── Procfile                # For deployment
├── runtime.txt             # For deployment
└── README.md               # This file
```

---

## 🚀 Future Improvements

- AI Chat Assistant
- Multi-language Support
- Payment Gateway Integration
- Team Collaboration
- Subscription Plans
- Analytics Dashboard
- REST API
- Docker Support

---

## 👨‍💻 Author

**Ahmad Arshad**

Feel free to connect and contribute to the project.