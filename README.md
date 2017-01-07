Flask Heroku Starter Kit
=======

<h1>Install Instructions</h1>
### Prerequisites
* python
* pip

### Configuration
After running new-flask-project, you'll need to change a few settings.

### Need a database?

Create your database.
* psql
* CREATE DATABASE <database_name>;

Change the configuration in your .env file:
export DATABASE_URL="postgresql://localhost/<database_name>"

Write your models. Then run:
* python manage.py db init
* python manage.py db migrate
* python manage.py db upgrade

Create your database on the server.
* heroku addons:create heroku-postgresql:hobby-dev --app <app_name>
* git push heroku master
* heroku run python manage.py db upgrade --app <app_name>

### Need users?

Your models will come with a User out of the box. Feel free to delete them if you don't need them.

### Need redis and a worker?

* heroku addons:create redistogo:nano --app <app_name>

In .env, change REDISTOGO_URL to a local redis on a different port. Then run a local redis server with:
* redis-sever --port <port>

### Need analytics?

In .env, change AMPLITUDE_KEY to your amplitude key. Then run:
* heroku config:set AMPLITUDE_KEY='<your_amplitude_key>'

### Need a landing page?

Use Bootstrap Studio to create your landing page. Then just export it in the directory of your project. Make sure you haven't already written stuff in the assets folder as it will replace this.


### Don't need any of this stuff?

Just delete the files.