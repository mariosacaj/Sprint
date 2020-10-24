# Development
#### Requirements
1. Install all the requirements: `pip install -r requirements.txt`.
2. Place the [google model](https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit) in `model/`.
3. Install JDK 11 or higher.
    * If you have multiple JDKs installed, you must set your `$JAVA_HOME` environment variable to a JDK >= 11.


Run server:
1. Run `python manage.py runserver`
2. Go to `http://127.0.0.1:8000`

# Production
#### Requirements
1. Install all the requirements: `pip install -r requirements.txt`.
2. Place the [google model](https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit) in `model/`.
3. Install JDK 11 or higher.
    * If you have multiple JDKs installed, you must set your `$JAVA_HOME` environment variable to a JDK >= 11.

Go to production:
1. Set `DEBUG = False` in `Sprint/settings.py`
2. Change `SECRET KEY` in `Sprint/settings.py`
3. `python manage.py makemigrations`
4. `python manage.py migrate`
5. `python manage.py collectstatic`
6. Install a static files server (like `nginx`) and a wsgi or asgi server (like `gunicorn`) and configure them:
    * `gunicorn` should point to the `Sprint/wsgi.py` or `Sprint/asgi.py` module and must import the `application` variable.
    * `nginx` should be set to serve on its own the static files (which will be located in `nginx/staticfiles` after instruction #5) and call `usgi` for every other request
    * `Apache` with `mod_wsgi` can also be used
    *  the `on_starting()` routine in `prestart.py` must be invoked by 
    `gunicorn` (or by the process handling the wsgi/asgi server) before the instantiation of the workers.


# Easy Deployment (with Docker)
Requires: docker-compose, docker

1. Place the [google model](https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit) in `model/`.
2. Edit `django.env` to your preference
3. Run `./deployment.sh`

### Pre-built images
If you don't want to build the docker images by yourself, you can use pre-built images

1. `docker pull mskx4/sprint_nginx`
2. `docker pull mskx4/sprint`
3.  Edit `django.env` to your preference
4. `docker-compose up -d`

# Warning
Please be aware that, when in `DEBUG` mode, only a small portion of the Google model is loaded (50K words).
When `DEBUG = False` the loading of the whole model eats up to 12 GB of RAM. Be sure to deploy in a
appropriate setting.