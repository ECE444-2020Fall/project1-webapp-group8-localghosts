# APPrentice

This is a repository for Group 8 (Localghosts)'s ECE444 project. 

## How to run

Using docker-compose:

```sh
# Build and run in foreground
docker-compose up --build
# Flask app should now be accessible at localhost:5000
# ctrl-c to kill
```

Note: the app is currently configured to run on the default Flask development server, but in the future it would be wise to deploy using a WSGI server (like [this](https://github.com/tiangolo/uwsgi-nginx-flask-docker) or [this](https://github.com/tiangolo/meinheld-gunicorn-flask-docker))

## How to test

Also provided in this repo is a `docker-compose.test.yml` file, which can be used as an override to run the `flask test` command instead of the `flask run` command. Here's how to run the tests:

```sh
# Build and run tests in foreground
docker-compose -f docker-compose.yml -f docker-compose.test.yml up --build
```

## Contribution guidelines

todo, but we should agree on things like unit tests and code formatting etc