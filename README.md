# APPrentice

This is a repository for Group 8 (Localghosts)'s ECE444 project. 

## How to run

Using docker-compose:

```sh
# Build and run in background (omit -d for foreground)
docker-compose up --build -d

# Flask app should now be accessible at localhost:5000

# Teardown
docker-compose down
```

Note: the app is currently configured to run on the default Flask development server, but in the future it would be wise to deploy using a WSGI server (like [this](https://github.com/tiangolo/uwsgi-nginx-flask-docker) or [this](https://github.com/tiangolo/meinheld-gunicorn-flask-docker))

## Contribution guidelines

todo, but we should agree on things like unit tests and code formatting etc