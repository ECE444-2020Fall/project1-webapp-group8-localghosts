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

### Restarting a single service

Once the entire app is up and running, you can restart individual services (e.g. when making changes to the Flask `app` without having to restart the `recipes` elasticsearch) as follows:

```sh
### TERMINAL 1 ###
# previous docker-compose up --build is still running

### TERMINAL 2 ###
docker-compose up --build app  # to rebuild and run the 'app' service
# ctrl-c to kill just the new service
```

## How to test

Also provided in this repo is a `docker-compose.test.yml` file, which can be used as an override to run the `flask test` command instead of the `flask run` command. Here's how to run the tests:

```sh
# Build and run tests in foreground
docker-compose -f docker-compose.yml -f docker-compose.test.yml up --build
```

## Contribution guidelines

todo, but we should agree on things like unit tests and code formatting etc