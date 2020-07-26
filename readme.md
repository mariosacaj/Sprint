#Requirements:
1. Create a conda environment using `environment.yml` to install all the requirements or use `requirements.txt` with pip. Conda is better.
2. Place the google model in `/model`, accordingly to the `readme.me` file you can find there.
3. Install Java 13.
4. Go to `annotator/tool/JavaLoad.py`.
5. Set the `jvmpath` value of the `jpype.startJVM()` function to the absolute path of your Java Virtual Machine (sometimes is not necessary to specify it as `jpype` finds it on its own).

Warning: Pycharm 2020.1 has a weird bug related to the `xml.dom.minidom` package dependency. It shouldn't be a problem though.

#Deployment:
###Development
Run `python manage.py runserver`

###Production
1. Set `DEBUG = False` in `Sprint/settings.py`
2. `python manage.py makemigrations`
3. `python manage.py migrate`
4. `python manage.py collectstatic`
5. Install `nginx` and `usgi` and configure them
    * `usgi` should point to `Sprint/wsgi.py`.
    * `nginx` should be set to serve on its own the static files and call `usgi` for every other request
    *  `Apache` with `mod_wsgi` can also be used
    *  IMPORTANT: `usgi` or `mod_wsgi` MUST be set to use 1 worker/process and many threads.