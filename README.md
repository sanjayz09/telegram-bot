# telegram-bot

### Config
Nginx + uWSGI + Flask

* Nginx
```
location = /yourapplication { rewrite ^ /yourapplication/; }
location /yourapplication { try_files $uri @yourapplication; }
location @yourapplication {
  include uwsgi_params;
  uwsgi_pass 127.0.0.1:3031;
}
```

* [uWSGI](https://flask.palletsprojects.com/en/1.0.x/deploying/uwsgi/)
```
uwsgi uwsgi.ini
```

uwsgi.ini
```
[uwsgi]
socket = 127.0.0.1:3031
chdir = ./
wsgi-file = wsgi.py
```
