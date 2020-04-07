# Getting Started
## Dependencies
What you need to run this app:

* `Python` and `Flask`.

* Ensure you're running the latest versions of Python `3.x` and Flask `1.x`.

> **Note:** For Mac users, it is recommended to first install **Homebrew**, as it will smooth the process of installing first dependencies. You can check it out [here](https://brew.sh/).

## Installing dependencies
1. First we need to have Python installed. For that, just run the command below:
```bash
$ brew install python
```
2. Now we will need to create a `virtual environment` inside our project. For that, we need to go to our project folder and install a `venv` folder inside:
```bash
$ cd covid19
$ python3 -m venv venv
```
3. Once the environment has been created, simply run it with the following command:
```bash
$ . venv/bin/activate
```
4. Now we will install `Flask`. Within the environment activated (you will notice a `(venv)` prefix on command line now), use the following command:
```bash
$ pip install Flask
```
> **Note:** For more information about Flask's installation, check the original [installation guide](https://flask.palletsprojects.com/en/1.1.x/installation/).

### Library dependencies
By now, all the dependencies needed to being able to run our project are installed. However, if you try to run the app now with `flask run`, you will be surprised by some unexpected errors such as `ModuleNotFoundError: No module named 'flask_wtf'`. This is because certain libraries used by the project are not installed automatically.
In order to install them, simply run the command:
```bash
$ pip install flask-assets flask-oidc flask-wtf pandas pyscss
```
> **Note:** Here are included only the dependencies required at the time this file was written. If more dependencies would be required, just refer to the [app.py](https://github.com/laramaktub/covid19/blob/master/app.py) file and check the modules imported.

### File dependencies
Same as happened with the [Library dependencies](#library-dependencies), certain additional files are required for the project to be able to run correctly:
* `client_secret.json` which contains `OAuth` credentials. Should be placed in the `root` folder
* `covid19.db` is a database file which contains test examples to work locally. Should be placed in the `./db` folder.
* An `img` folder which shall contain a set of X-Ray images to test the cases stored in the  _covid19.db_ file. This folder should be placed in the `./static` folder.
> **Note:** In order to get those files, please request them through the email shared in the [contact us](#contact-us) section.

## Running the app
Now that we have installed all dependencies and we have our virtual environment activated, it's time to run the project:
```bash
$ flask run
```
> **Note:** The project will most probably be running in http://localhost:5000/


### Detecting changes
Sometimes, while running and making changes, the app does not refresh automatically, specially if changes relate to `template` or `static` files (`.js`, `.css`, etc).
* In case of `.css` files, simply full refresh `localhost` by pressing `SHIFT+Cmd+R` or by clicking refresh button while pressing `SHIFT`.
* For `.html` files, sames steps described above, but right after entering `flask run` again.

# Useful Information
## Use a Flask-aware editor
These are some well known editors which can be used to edit the project:

* [Visual Studio Code](https://code.visualstudio.com/)
* [Atom](https://atom.io/) with [Flask plugin](https://atom.io/packages/flask-snippets)


## Further Information
For more about Flask and Jinja, you can refer to the [user's guide](https://flask.palletsprojects.com/en/1.1.x/)


### Contact us

* Generic mail: covid19trainingapp@gmail.com
