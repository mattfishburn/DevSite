# DevSite
This is my toy project for learning about django.

Register is a toy registration email app.  It uses python3 and django
1.9.7, please make sure these are on your local path. To run it,
download this repo, create a local database by running:

python manage.py makemigrations register
python manage.py migrate

You will also need to edit the EMAIL_* variables in the settings.py to
point to an email server.  The default values work for a local install
of postfix.  Finally, run

python manage.py runserver

and point your browser to

http://127.0.0.1:8000/register/