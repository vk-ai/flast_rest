# End to End implementation of Flast REST API

Features

1. Folder Structure
2. Tests (Pytest and coverage)
3. Blueprints
    Blueprints helps to create different modules that then we can register with our main Flask App so we can keep our application modular

4. Flask SQLAlchemy
5. File-based database (sqlite)
6. HTTP status code
7. Validators
8. JWT Tokenization (Authentication)
9. Pagination
10. CRUD operations
11. Flask API error handling
12. Swagger Documentation

## How to run the application
1. Git clone
2. pip install virtualenv
3. python<version> -m venv <virtual-environment-name> (Ex: python3.8 -m venv env)
4. source <virtual-environment-name>/bin/activate (Ex: source env/bin/activate)
5. pip install -r requirements.txt
6. Run command flask run

## Run Test
1. pytests
2. coverage run -m pytest
3. coverage report

## How to run the application using docker
1. docker build -t flask-app .
2. docker run -it -p 3000:3000 -d flask-app