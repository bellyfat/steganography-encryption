# Stegano Encrypto

### Running
1. Clone the repo : 
```bash
$ git clone https://gitlab.com/sreecodeslayer/stegano-encrypto.git
$ cd stegano-encrypto
```
2. Create database : `stegano` in postgres
```psql
psql> CREATE DATABASE stegano;
```
3. Install requirements in a virtual env of Python 3.6+
```bash
$ pip install -r requirements.txt
```  
4. Run migrations
```bash
$ export STEGANO_ENV=dev
$ export FLASK_APP=run.py
$ flask db init
$ flask db migrate
$ flask db upgrade
```
5. Running API via gunicorn (You may wanna configure you email service)
```bash
$ export MAIL_USERNAME='your email id'
$ export MAIL_PASSWORD='your email password'
$ pip install gunicorn
$ gunicorn run:application -w 4
```

Configurations regarding Postgres Connection is inside `stegano/config.py` and can be configured as per the needs.  
Currently the app will try to connect with `postgres:postgres` to `localhost`

> This project was initiated using the cookiecutter from my github [repo](https://github.com/sreecodeslayer/cookiecutter-flask-restful)