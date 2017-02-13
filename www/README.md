Files under the `www` directory are supportive files for the serving platform.

* nginx.conf - virtual host configuration
* wsgi.py - wsgi bootstrap
* static/index.html - privacy policy (required by Google Home)
* bin/gunicorn_start.sh - init file for gunicorn + wsgi + flask + python virtual env
