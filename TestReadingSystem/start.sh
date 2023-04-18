ps -aux | grep python|xargs kill -9
nohup python manage.py runserver 0.0.0.0:8000