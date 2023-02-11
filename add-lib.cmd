"C:\Program Files\Python311\python.exe" -m pip install --upgrade pip
"C:\Program Files\Python311\python.exe" -m pip install -r requirements.txt
cd app
start chrome http://127.0.0.1/admin/
"C:\Program Files\Python311\python.exe" ./manage.py runserver 80