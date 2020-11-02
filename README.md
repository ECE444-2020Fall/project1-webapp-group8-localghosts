# APPrentice

This is a repository for Group 8 (Localghosts)'s ECE444 project. 

## How to run

These instructions assume you're in the root directory of the repo:

```sh
cd path/to/project1-webapp-group8-localghosts
```

### Running the full application

You can run the full app using docker-compose:

```sh
# Build and run in foreground
docker-compose up --build

# Flask app should now be accessible at localhost:5000 once Elasticsearch is up
# Elasticsearch should be accessible at localhost:9200 (takes a few seconds to start up, please wait)

# ctrl-c to kill
```

Note: the app is currently configured to run on the default Flask development server, but in the future it would be wise to deploy using a WSGI server (like [this](https://github.com/tiangolo/uwsgi-nginx-flask-docker) or [this](https://github.com/tiangolo/meinheld-gunicorn-flask-docker))

### Running the full application in development mode

Also provided in this repo is a `docker-compose.dev.yml` file, which can be used as an override to watch your filesystem for changes and automatically restart the flask app if any are detected. This means you can run the below command once and not have to rebuild/restart the containers every time you make a change to your flask app:

```sh
# Build and run in foreground with the development configuration
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build

# The flask app should restart every time you re-save a file now
# ctrl-c to kill as usual
```

## How to test

Also provided in this repo is a `docker-compose.test.yml` file, which can be used as an override to run the `flask test` command instead of the `flask run` command. Here's how to run the tests:

```sh
# Build and run tests in foreground
docker-compose -f docker-compose.yml -f docker-compose.test.yml up --build --exit-code-from app
```

## Contribution guidelines

todo, but we should agree on things like unit tests and code formatting etc