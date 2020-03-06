# TypeWriter
A powerful and customizable blog/weblog system written in Python Django supporting multiple languages for posts

## Requirements
  - python (version 3 or higher)
  - pip
  - gettext
  - a database (e.g. MariaDB, MySQL, postgresql, ...)
  - either a webserver like nginx or apache as reverse proxy or uwsgi for deployment

### PIP Requirements
  - django
  - django-ckeditor
  - mysqlclient (or the equivalent package for your database)

## Installation instructions
  1. Install all requirements
  2. Pull this repository
  3. Create a new database and database user
  4. Edit in the settings.py things like database connection, upload paths, static paths, allowed IP addresses and possible languages
  5. Create the database structure with `python3 manage.py migrate`
  6. Create the translation file with `python3 manage.py compilemessages`
  7. Create a new superuser with `python3 manage.py createsuperuser`
  8. Log into admin page and add things like languages, one settings object and the translated and translatable objects
  9. Run or deploy the project as you wish
