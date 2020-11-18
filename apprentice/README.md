# APPrentice

This is a repository for Group 8 (Localghosts)'s ECE444 project. 

The application structure is heavily borrowed from [Miguel Grinberg's Flask Web Development textbook](https://github.com/miguelgrinberg/flasky).

**NOTE**: this README details how to run the application baremetal. For the recommended way (using Docker), see the top-level README in this repository.

## Getting started

Create a Python `virtualenv` and install the dependencies:

```sh
cd /path/to/repo

python -m venv venv

# Bash-like shells
source ./venv/bin/activate

# Windows
.\venv\Scripts\activate

pip install -r requirements.txt
```

To run the APPrentice application, first set [the environment variables for the application](https://flask.palletsprojects.com/en/1.1.x/cli/):

```sh
# Bash-like shells
export FLASK_APP=apprentice.py

# Windows CMD:
set FLASK_APP=apprentice.py

# Windows PowerShell:
$env:FLASK_APP = "apprentice.py"
```
The first time you run the application, you'll have to create the SQLite tables. **I'm not sure if these should go into version control**, but I guess it depends on what we're going to store in the files (i.e. recipes=yes, user data=no).

```python
# In the OS shell
flask shell

# In the Python shell
db.create_all()
exit()
```

Finally, run your application. You can view the page at [localhost:5000](http://localhost:5000/).

```sh
# after setting FLASK_APP
flask run
```

Note for developers: 

To be able to carry out the Google Image Searches (for invalid OpenRecipes Image URLs), a ".env" file with the following content needs to be added to the root directory of the project.

GCS_DEVELOPER_KEY=`<GCS api key>`

GCS_CX=`<GCS Search engine ID>`
