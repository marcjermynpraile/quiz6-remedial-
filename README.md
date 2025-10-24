🚗 Ride Booking System (Django)

A simple ride-booking web application built with Django, allowing customers to book rides, riders to accept them, and admins to manage the platform.

📋 Features

User registration and login (Customer & Rider)
Book rides with pickup & destination
Automatic random distance (10–30 km)
Price calculated based on distance
Rider dashboard for accepting/completing rides
Customer dashboard for viewing booked rides
Balance management for payments

🧰 Prerequisites

Make sure you have installed:

Python 3.10+

Git

🧑‍💻 1. Clone the Repository

Open your terminal or command prompt, then run:

git clone https://github.com/your-username/ride_booking_angeles.git
cd ride_booking_angeles


💡 Replace your-username with your GitHub username if you forked or uploaded the project.

🏗️ 2. Set Up a Virtual Environment
Windows:
python -m venv .venv
.venv\Scripts\activate

macOS / Linux:
python3 -m venv .venv
source .venv/bin/activate

📦 3. Install Dependencies
pip install -r requirements.txt


If requirements.txt doesn’t exist yet, create one with:

pip freeze > requirements.txt

🗄️ 4. Set Up the Database

Since the database file (db.sqlite3) may not exist yet, initialize it by running:

python manage.py makemigrations
python manage.py migrate

👤 5. Create User Accounts
🔸 Create a Superuser (Admin)
python manage.py createsuperuser


Then visit:
👉 http://127.0.0.1:8000/admin/

and log in using your admin credentials to manage rides, users, and balances.

🔹 Register Normal Users

Alternatively, start the server and register via the website:

python manage.py runserver


Then open your browser:

Customer Registration → http://127.0.0.1:8000/accounts/register/

Rider Registration → http://127.0.0.1:8000/accounts/rider/register/