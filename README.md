# Habital - Personal Habit Tracker Web App

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)

**Habital** has evolved! What started as a database practice project is now a fully functional **SaaS (Software as a Service) Application**. It allows users to create accounts, log in securely, and track their daily habits with a persistent cloud database.

## New Features (v2.0)

* **Secure Authentication:** Complete Login/Register system using `Flask-Login` and Password Hashing.
* **Cloud Database:** Migrated from local SQL to **Neon Tech (PostgreSQL)** in the cloud.
* **Modern UI:** A responsive dark-mode interface built with **Bootstrap 5** and **Pico.css**.
* **Security Best Practices:** Environment variables (`.env`) for sensitive credentials.

## Technical Stack

* **Backend:** Python, Flask, Gunicorn.
* **Database:** PostgreSQL (Production), Psycopg2.
* **Frontend:** HTML5, CSS3, Jinja2 Templates.
* **Hosting:** Render (App) + Neon (DB).

## How to Run Locally

1.  **Clone the repository**
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configure Environment:**
    Create a `.env` file with your credentials:
    ```ini
    DATABASE_URL=your_neon_url_here
    SECRET_KEY=your_secret_key
    ```
4.  **Initialize Database:**
    ```bash
    python init_db.py
    ```
5.  **Run:**
    ```bash
    python app.py
    ```

---
*Built by Jeipyy as part of a Project-Based Learning journey.*