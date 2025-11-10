# Newsletter Demo App

A demo project that allows a user to create and manage multiple newsletters with individual subscription pages, subscriber management, and bulk email sending functionality.

---

## Overview

This project demonstrates a simple implementation of a newsletter management system.

Each newsletter has:
- Its own unique subscription page.
- A dedicated subscriber list.
- Managing subscribers.
- Functionality for sending bulk emails to all subscribers.

---

## Features

- Create and manage multiple newsletters.
- Automatically generate subscription pages for each newsletter.
- Add and manage subscribers.
- Send bulk emails to newsletter subscribers.

---

## Tech Stack

- **Backend:** Python, Django  
- **Database:** SQLite for development
- **Frontend:** HTML, CSS (with template-based rendering), HTMX  
- **Email Handling:** Django Email Backend or SMTP  
- **Optional:** Celery for background email sending  

---

## Tech Stack
- [Django](https://www.djangoproject.com/) – Web framework  
- [HTMX](https://htmx.org/) – Dynamic interactivity without heavy JS  
- [Bootstrap](https://getbootstrap.com/) – Responsive UI framework  
- SQLite (default) 

---

## Installation & Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/Minenhle-Ngubane/newsletter
   cd newsletter

2. **Create and activate a virtual environment**
    ```python -m venv venv
        # Activate virtual environment
        # On Linux/Mac:
        source venv/bin/activate
        # On Windows:
        venv\Scripts\activate
    ```

3. **Install dependencies**
    ```pip install -r requirements.txt```

4. **Apply migrations**
    ```python manage.py migrate```

5. **Create a superuser (admin)**
    ```python manage.py createsuperuser```

6. **Run the development server**
    ```python manage.py runserver```

7. **Access the app**
   - Open your browser and visit:
      http://127.0.0.1:8000/
