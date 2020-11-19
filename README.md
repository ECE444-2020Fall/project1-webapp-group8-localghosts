# APPrentice

This is a repository for Group 8 (Localghosts)'s ECE444 project. 
The application is deployed to Azure and can be found here: http://localghosts.eastus.cloudapp.azure.com/

## How to run

These instructions assume you're in the root directory of the repo:

```sh
cd path/to/project1-webapp-group8-localghosts
```

### Running the full application in production mode

You can run the full app using docker-compose (alternatively run it in a single-node swarm to simulate something closer to the production environment):

```sh
# Pull and run in foreground
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up

# Application should be accessible at localhost:80 once the necessary services are up
# ctrl-c to kill
```

The app is sitting behind an `nginx` reverse proxy and run with a `gunicorn` WSGI server. To hit the app (or other services) directly, see the development mode instructions in the next section.

### Running the full application in development mode

Also provided in this repo is a `docker-compose.dev.yml` file, which can be used as an override to watch your filesystem for changes and automatically restart the flask app if any are detected. This means you can run the below command once and not have to rebuild/restart the containers every time you make a change to your flask app:

```sh
# Build and run in foreground with the development configuration
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build

# Flask app should now be accessible at localhost:5000 once Elasticsearch is up
# Elasticsearch should be accessible at localhost:9200 (takes a few seconds to start up, please wait)

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

- All Unit tests must pass before a branch can be merged into develop.
- All new code must have unit tests before it can be merged. 
- Code needs to be formatted as follows:
    - Imports need to be sorted using **isort**
    - **Black** should be used for formatting
    - Frontend code (js/css/html) needs to be beautified using **js-beautify**
The code formatting and tests will be enforced on PR through the use of GitHub actions.
