# TechStartPro - Matheus Abreu

## Hello, i'm Matheus Abreu! <img src="https://raw.githubusercontent.com/MartinHeinz/MartinHeinz/master/wave.gif" width="30px">

This is my application to the TechStartPro program @ [Olist](https://olist.com/) that got me hired! :grin:
<br>

You can find a deployed version and the full API Docs, hosted at Heroku: http://olist.matheusabreu.com.br/

The original instructions can be found [here](INSTRUCTIONS.md).

## Contents

- [Contents](#contents)
- [Setup](#Setup)
- [Running](#running-the-application)
- [Importing Categories](#importing-categories)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Work Environment](#work-environment)

## Setup

After you clone this project, you can open the folder `tech_start_pro` in your favourite IDE or code editor.

### Docker

If you prefer, there's a docker ready option that will build and run the application with one single command.

You must have Docker and Docker Compose installed for this option two work.

Obs: Make sure you're in the right folder. The main project folder (`tech_start_pro`), which contains the `docker-compose.yaml` file.

```
docker-compose up -d
```

You can now access the application and full API documentation at `http://localhost:8000/`.

### Virtual Environment

To setup the virtual environment (i'm using pipenv here) you must run the following commands on your preffered terminal:

Obs: Make sure you're in the right folder. The main project folder (`tech_start_pro`), which contains the `manage.py` file.

Install Pipenv:

```
pip install pipenv
```

Install Dependencies:

```
pipenv install
```

### Env File

Now, you need to create a file named `.env` inside the project folder. You can find an example of how your file should look like bellow or in the file `sample.env`.

```
SECRET_KEY=SOME-SECRET-KEY # Must be a random generated string.
APP_DOCS_URL=http://127.0.0.1:8000/ $ The URL to your docs page, normally the root URL of the api.
```

### Populating Our Database

Next you will run the migrations, django will create a SQLite file and populate it with our tables. It sounds complicated, but we only need one command 😀.

Obs: Make sure you're in the right folder. The main project folder (`tech_start_pro`), which contains the `manage.py` file.

```
python manage.py migrate
```

## Running The Application

Use the following command:

Obs: Make sure you're in the right folder. The main project folder (`tech_start_pro`), which contains the `manage.py` file.

```
python manage.py runserver
```

... and that's it!

You can now access the application and full API documentation at `http://localhost:8000/`.

## Importing Categories

You can import categories from a csv file. The csv file has to follow the structure shown bellow.

```
name
Toys
Cellphones
Computers
```

To import a csv file, you'll have to use the following command:

```
python manage.py import_categories <path_to_csv_file>
```

Obs: Make sure you're in the right folder. The main project folder (`tech_start_pro`), which contains the `manage.py` file.

The proccess may take a while, depending on the size of the file you're importing. At the end, it will output `Finished!` in the terminal, to let you know everything went right. If there's any duplicate categories, you'll see a warning telling you which category is duplicated, but it will not interrupt the process nor write duplicates to the database.

## API Documentation

You can access the API documentation by visiting `http://127.0.0.1:8000/`, if you didn't change the default port, or accessing the deployed version at Heroku [here](http://olist.matheusabreu.com.br/).

## Testing

### Install ChromeDriver
In order to run functional tests with selenium, you'll need to download and install the chrome driver recommended for your Google Chrome version.

You can find how to download it visiting the official page [here](https://sites.google.com/a/chromium.org/chromedriver/downloads).

Afterwards, you shoul put the downloaded file in your system PATH env variable.

### Running Tests
Before running any tests, make sure the application is running, otherwise the docs tests made with selenium will fail.

#### Run all tests with coverage:

Obs: Make sure you're in the right folder. The main project folder (`tech_start_pro`), which contains the `manage.py` file.

```
coverage run --source='.' manage.py test
```

#### Generate coverage report:

```
coverage report
```

## Work Environment

**OS**: Linux Mint<br>
**IDE**: Pycharm Professinal 2020.2<br>
**Computer**: Dell Latitude 3400<br>
**Libaries**: Django, Django Rest Framework, Django-Filter, Python-Decouple, Def-Yasg, Coverage and Selenium. The Heroku deployed version uses all the already mentioned libraries plus: Django-Heroku, Psycopg2 (Postgres) and Gunicorn.
