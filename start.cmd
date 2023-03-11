IF EXIST "venv\Scripts\activate.ps1" (
    venv\Scripts\activate
    cd app
    start chrome http://127.0.0.1/admin/
    python manage.py runserver 80
) ELSE (
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    cd app
    start chrome http://127.0.0.1/admin/
    python manage.py runserver 80
)
