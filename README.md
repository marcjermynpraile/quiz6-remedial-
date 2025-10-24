# 🚗 Ride Booking System (Django)

A simple ride-booking web application built with Django, allowing customers to book rides, riders to accept them, and admins to manage the platform.

---

## 📋 Features

- User registration and login (Customer & Rider)  
- Book rides with pickup & destination  
- Automatic random distance (10–30 km)  
- Price calculated based on distance  
- Rider dashboard for accepting/completing rides  
- Customer dashboard for viewing booked rides  
- Balance management for payments  

---

## 🧰 Prerequisites

Make sure you have installed:

- **Python 3.10+**  
- **Git**

---

## 🧑‍💻 1. Clone the Repository

Open your terminal or command prompt, then run:

```bash
git clone https://github.com/your-username/ride_booking_angeles.git
cd ride_booking_angeles

🏗️ 2. Set Up a Virtual Environment
Windows: python -m venv .venv
.venv\Scripts\activate

macOS / Linux:
python3 -m venv .venv
source .venv/bin/activate
📦 3. Install Dependencies
pip install -r requirements.txt


If requirements.txt doesn’t exist yet, create one with:

pip freeze > requirements.txt

🎨 4. Install Django Crispy Forms (Bootstrap 5)

To enable modern and clean form styling, install crispy-bootstrap5:

pip install django-crispy-forms crispy-bootstrap5


Then, in your settings.py, add:

INSTALLED_APPS = [
    'crispy_forms',
    'crispy_bootstrap5',
    ...
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

🗄️ 5. Set Up the Database

If the db.sqlite3 file doesn’t exist yet, initialize it by running:

python manage.py makemigrations
python manage.py migrate

👤 6. Create User Accounts
🔸 Create a Superuser (Admin)
python manage.py createsuperuser


Then visit:
👉 http://127.0.0.1:8000/admin/

and log in using your admin credentials to manage rides, users, and balances.

🔹 Register Normal Users

Alternatively, start the development server:

python manage.py runserver


Then open your browser:

Customer Registration: http://127.0.0.1:8000/accounts/register/

Rider Registration: http://127.0.0.1:8000/accounts/rider/register/

🚀 7. Run the Application

Start the server with:

python manage.py runserver


Visit the app in your browser:
👉 http://127.0.0.1:8000/

💾 8. (Optional) Save Requirements

Whenever you install new packages (like crispy forms), update your requirements:

pip freeze > requirements.txt

🛠️ Troubleshooting

If you encounter migration errors:

python manage.py migrate --run-syncdb


If styles are missing, ensure crispy-bootstrap5 is installed and added to INSTALLED_APPS.
