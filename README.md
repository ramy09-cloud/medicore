# MediCore - Patient Diagnosis System (Django)

Login: username **user**, password **user** (works for the site and the admin panel).

## Run
```
pip install -r requirements.txt
python manage.py runserver
```
Open http://127.0.0.1:8000  (admin panel: http://127.0.0.1:8000/admin/)

db.sqlite3 already has the tables, the login above and some sample records.
To start with an empty database: delete db.sqlite3, then run
`python manage.py migrate` and `python manage.py createsuperuser`.

## Structure
- `medicore/` settings package (settings.py, urls.py with ALL the URLs)
- `clinic/` the app (models.py, forms.py with the ModelForms, views.py, admin.py)
- `templates/` one page per file (index.html = dashboard)
- `static/` Bootstrap 4 (css/bootstrap.min.css, js/bootstrap.bundle.min.js), jQuery, Tabler icons, style.css

## Templates
- Site: layout based on **Tabler** (https://tabler.io), rebuilt on Bootstrap 4.
- Admin panel: **Jazzmin** (https://github.com/farridav/django-jazzmin).
