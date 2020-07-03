####`urls.py` imports `views.py`
In `urls.py` every possible url is mapped to a view function in `views.py`.

####`views.py` imports `models.py`
Databases schema are accessed directly in `views.py`. To convert classes in models.py into actual schemas do the following:

`$ python manage.py makemigrations`

`$ python manage.py migrate`
