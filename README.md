# Travel2India 🇮🇳

Travel2India is a modern, responsive Django-based web application designed to showcase the beauty, culture, and rich heritage of India. It helps travelers explore top destinations, book flights, send customized trip inquiries, make secure online payments, and chat with an automated travel assistant.

---

## 🚀 Features

- **17 Curated Destinations**: Explore detailed guides for places like Kerala Backwaters, Ladakh, Goa, Jaipur, Varanasi, and more—featuring best times to visit, must-see spots, and suggested durations.
- **Dynamic Search Engine**: A multi-word matching search bar that allows users to query by destination name or keywords (e.g., searching "golden temple" returns Amritsar).
- **Responsive Card Grids**: Beautifully styled grid system using CSS Grid and Bootstrap, optimized for seamless viewing on desktops, tablets, and mobile screens.
- **Trip Inquiry & Flight Booking Forms**: Custom forms that capture travel details and automatically notify the admin via formatted email notifications.
- **Secure Payments Integration**: Integrates the **Razorpay Checkout SDK** (cards, netbanking, UPI) with secure backend verification.
- **Interactive Chatbot Widget**: A client-side automated chatbot that helps users navigate, find information, and link directly to planning pages.
- **Dark Mode Support**: Global theme toggle to switch between a bright, clean design and a sleek dark theme.

---

## 🛠️ Technology Stack

- **Backend**: Python 3.12, Django 5.1.6
- **Frontend**: HTML5, Vanilla CSS3 (Custom Styles), JavaScript (ES6), Bootstrap 5.3
- **Database**: PostgreSQL (Production) / SQLite3 (Local Development)
- **Payment Gateway**: Razorpay Web SDK
- **Static Assets Management**: WhiteNoise (compresses and caches static assets for production)
- **Server Gateway**: Gunicorn (WSGI HTTP server for production)

---

## 💻 Local Development Setup

Follow these steps to run the project on your local machine:

### 1. Clone the Repository
```bash
git clone https://github.com/Ateeb09/Travel2India.git
cd Travel2India
```

### 2. Set Up a Virtual Environment
Create and activate a Python virtual environment:
```bash
# On Windows
python -m venv .venv
.venv\Scripts\activate

# On macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r travel2india/requirements.txt
```

### 4. Create your `.env` File
Create a `.env` file inside the `travel2india/` subdirectory (use `travel2india/.env` as a template) and add your local test keys:
```env
# Razorpay Credentials
RAZORPAY_KEY_ID=rzp_test_yourKeyHere
RAZORPAY_KEY_SECRET=yourSecretKeyHere

# Admin Email Notifications (Optional)
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
```

### 5. Apply Database Migrations
```bash
cd travel2india
python manage.py migrate
```

### 6. Start the Development Server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser.

---

## 🌐 Production Deployment on Render

This project is fully configured for deployment on **Render** (using PostgreSQL and WhiteNoise).

### Render Configuration Steps:

1. **Web Service Setup**:
   - **Environment**: `Python`
   - **Build Command**: `./build.sh` (or `bash build.sh`)
   - **Start Command**: `gunicorn travel2india.wsgi`

2. **Database Link**:
   - Create a **Render PostgreSQL** database service.
   - Link it to your Web Service (this will automatically inject the `DATABASE_URL` environment variable).

3. **Required Environment Variables**:
   Under the **Environment** tab of your Render Web Service, add the following:
   - `RAZORPAY_KEY_ID`: Your live/test Razorpay API Key ID.
   - `RAZORPAY_KEY_SECRET`: Your live/test Razorpay Key Secret.
   - `EMAIL_HOST_USER`: Your Gmail address (for sending notifications).
   - `EMAIL_HOST_PASSWORD`: Your Gmail App Password (secure 16-character code).
   - `DJANGO_SECRET_KEY`: A unique secure string for production cryptography.
   - `DJANGO_DEBUG`: Set to `False` in production.
