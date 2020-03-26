# Quick start with Python Flask Framework
Basic curd RESTful API with FLask
### Setting environments
```sh
$ mkdir flaskapp
$ python3 -m venv flaskapp
$ cd flaskapp
$ source bin/activate
$ git clone lhttps://github.com/duchau97kma/LearnFlaskPython.git repo
$ cd repo
```
### Install
```sh
$ pip install Flask
$ pip install psycopg2-binary
$ pip install flask-sqlalchemy
$ pip install Flask-Migrate
```
### Create database
```sh
$ sudo su postgres
$ psql
$ postgres=# create database testdb;
$ postgres=# create user winter  with password '12345';
$ postgres=# GRANT ALL PRIVILEGES ON DATABASE testdb to winter;
```
### Run test
Before you can do that you need to tell your terminal the application to work with by exporting the FLASK_APP environment variable

```sh
$ flask run
```
### Migrate Model to Database
```sh
$ flask db init 
$ flask db migrate 
$ flask db upgrade
```
### Learn more
  - [FLASK documentation](https://flask.palletsprojects.com/en/1.1.x/)
  - [SQLAlchemy](https://docs.sqlalchemy.org/en/13/orm/tutorial.html)
