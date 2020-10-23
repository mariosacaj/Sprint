# Requirements:
1. Install all the requirements: `pip install -r requirements.txt`.
2. Place the [google model](https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit) in `/model`.
3. Install JDK 11 or higher.
    * If you have multiple JDKs installed, you must set your $JAVA_HOME environment variable to a JDK >= 11.

# Development 
1. Run `python manage.py runserver`
2. Go to `http://127.0.0.1:8000`

# DIY Deployment
1. Set `DEBUG = False` in `Sprint/settings.py`
2. Change `SECRET KEY` in `Sprint/settings.py`
2. `python manage.py makemigrations`
3. `python manage.py migrate`
4. `python manage.py collectstatic`
5. Install static server (like `nginx`) and wsgi or asgi server (like `usgi`) and configure them
    * `usgi` should point to `Sprint/wsgi.py`.
    * `nginx` should be set to serve on its own the static files (which will be located in `nginx/staticfiles` after instruction #4) and call `usgi` for every other request
    *  `Apache` with `mod_wsgi` can also be used

Please be ware that, when in DEBUG mode, only a small portion of the Google model is loaded (50K words).

# Easy Deployment (with Docker)
