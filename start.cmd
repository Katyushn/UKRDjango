IF EXIST "C:\Program Files\Python311\python.exe" (
    venv\Scripts\activate
    cd app
    start chrome http://127.0.0.1/admin/
    python manage.py runserver 80
) ELSE (
    python-3.11.1-amd64.exe InstallAllUsers=1 PrependPath=1 Include_test=0 SimpleInstall=1
    gettext0.21-iconv1.16-static-64.exe
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    cd app
    start chrome http://127.0.0.1/admin/
    python manage.py runserver 80
)
