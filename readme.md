# Requirements:
1. Create a conda environment using `environment.yml` to install all the requirements or use `requirements.txt` with pip (Note: mkl_fft may not be available, depending on the installed version of Python (also see [here](https://github.com/IntelPython/mkl_fft/issues/26)). Conda is better.
   * As an alternative, it is possible to create a new conda environment, to activate it, to install pip using conda and to install the requirements using pip
2. Place the google model in `/model`, accordingly to the `readme.me` file you can find there.
3. Install JDK 11 or higher.


# Deployment:
### Development
1. Run `python manage.py runserver`
2. Go to `http://127.0.0.1:8000`

### Production
1. Set `DEBUG = False` in `Sprint/settings.py`
2. `python manage.py makemigrations`
3. `python manage.py migrate`
4. `python manage.py collectstatic`
5. Install `nginx` and `usgi` and configure them
    * `usgi` should point to `Sprint/wsgi.py`.
    * `nginx` should be set to serve on its own the static files (which will be located in `/staticfiles` after instruction #4) and call `usgi` for every other request
    *  `Apache` with `mod_wsgi` can also be used

Please be ware that, when in DEBUG mode, only a small portion of the Google model is loaded (50K words).