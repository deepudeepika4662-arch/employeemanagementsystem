# Employee Management System

A professional Django application for employee table operations using Django's default SQLite database. This project is built to manage employee data only — no student-related functionality is included.

## What this project does

- Implements employee table functions using Django models and views
- Uses Django's built-in SQLite backend (`db.sqlite3`) only
- Performs employee CRUD operations on the `Employee` table
- Provides secure login/logout functionality for employees and admins
- Offers role-based access control: employees see only their own records, admins see all records
- Includes a polished Bootstrap-based frontend for all employee pages

## Employee features

- Add employee records
- Edit employee records
- Delete employee records
- Search employee records by `full_name`, `email`, or `department`
- View employee profile and manage personal data
- Admin dashboard to manage all employee records

## Employee table fields

The app stores employee data in a table with these fields:

- `employee_id` — unique integer identifier
- `full_name`
- `email`
- `department`
- `age`
- `user` — linked user account for profile access
- `created_by` — owner of the employee record

## Project structure

- `employee_management/` — Django project settings and URL configuration
- `employees/` — Django app with employee models, forms, views, and templates
- `templates/employees/` — frontend templates for employee pages
- `static/css/style.css` — custom UI styling for a professional appearance

## Setup

1. Create and activate a virtual environment

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

2. Install dependencies

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

3. Apply migrations

```powershell
python manage.py migrate
```

4. Create a superuser

```powershell
python manage.py createsuperuser
```

5. Start the development server

```powershell
python manage.py runserver 127.0.0.1:8000
```

6. Open in browser

- App: `http://127.0.0.1:8000/`
- Employee list: `http://127.0.0.1:8000/employees/`
- Add employee: `http://127.0.0.1:8000/employees/add/`
- Employee detail: `http://127.0.0.1:8000/employees/detail/<id>/`
- CBV list: `http://127.0.0.1:8000/employees/cbv/`
- Login: `http://127.0.0.1:8000/employees/login/`
- Admin: `http://127.0.0.1:8000/admin/`

## Notes

- Uses Django default SQLite (`db.sqlite3`) only — no external database.
- Keep `DEBUG = False` and set `ALLOWED_HOSTS` before production deployment.
- Replace `SECRET_KEY` in `employee_management/settings.py` before deploying to production.

## Recommended commands

```powershell
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 127.0.0.1:8000
```
