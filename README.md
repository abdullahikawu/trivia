# Trivia App

Trivia is a web application created for trivia games as a way of building the bonds between students and employees of Udacity. The trivia application is built with an API endpoints that enables the trivia  to create, fetch and update data needed the application.

## Getting Started
The project frontend built using react is designed to work with Flask-based Backend.

### Prerequisites

- Frontend 
1. NodeJS

- Backend
1. Python 3.8
2. Virtual Environment
3. Postgresql

### Installations

- Step 1: Install Required Software
Python 3.7 - Follow instructions to install the latest version of python for your platform in the python docs

Virtual Environment - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the python docs

Postgres - If you don't already have it installed, see installation instructions for your operating system here:PostgreSQL Downloads

NodeJS - Required to serve the frontend. The frontend app was built using create-react-app and uses NPM to manage software dependencies.

- Step 2: Extract the project zip file to a directory you want to place the project.

- Step 3: Install frontend Dependenciees 
After the zip extraction is complete, Navigate to the frontend directory which can be found on the project root directory and run the following commands to install frontend dependencies:

npm install

- Step 4: Create a virtual environment
cd into the `backend` directory which can be found at the project root directory and create a virtual environment with the following commands:

python3 -m venv env
source env\bin\activate

- Step 5: Install backend Dependencies
 In the `backend` directory run the following commands to install the required dependencies:

pip install -r requirements.txt

- Step 6: Set up and Populate the Database
Setup your production and test database.

Start the postgres server with the following command:

sudo systemctl start postgresql.service

Next, create a trivia database:

createdb trivia
createdb trivia_test

From the backend folder in terminal, Populate both trivia and trivia_test database using the trivia.psql file provided. run:

psql trivia < trivia.psql
psql trivia_test < trivia.psql

### Start the Server
While in the virtual environment is activated. Navigate to the backend directory, start the  backend Flask server by running:

export FLASK_APP=flaskr
export FLASK_ENV=development
flask run

In the fronend directory, start the frontend server by running:

npm start

### Run API test
To run API test, navigate to the backend directory and run the commands below:

python3 test_flaskr.py

## API Reference
Trivia backend server runs on localhost with the base URL: localhost:5000 

### Error status codes and message
400 - Invalid request
422 - unprocessable
404 - Request not found
500 - Server error

- Error response example
{
    'success': False,
    'error': 404,
    'message': 'Request not found'
}

### API Endpoints

#### GET '/categories'

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains an object of id: category_string key:value pairs.
{
    'success': True,
    'categories': { '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports" }
}
#### GET '/questions?page=${integer}'

- Fetches a paginated set of questions, a total number of questions, all categories and current category string.
- Request Arguments: page - integer
- Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string

{
    'success': True,
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer',
            'difficulty': 5,
            'category': 2
        },
    ],
    'totalQuestions': 100,
    'categories': { '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports" },
    'currentCategory': 'History'
}


#### GET '/categories/${id}/questions'

- Fetches questions for a cateogry specified by id request argument
- Request Arguments: id - integer
- Returns: An object with questions for the specified category, total questions, and current category string

{
    'success': True,
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer',
            'difficulty': 5,
            'category': 4
        },
    ],
    'totalQuestions': 100,
    'currentCategory': 'History'
}


#### DELETE '/questions/${id}'

- Deletes a specified question using the id of the question
- Request Arguments: id - integer
- Returns: Does not need to return anything besides the appropriate HTTP status code. Optionally can return the id of the question. If you are able to modify the frontend, you can have it remove the question using the id instead of refetching the questions.


#### POST '/quizzes'

- Sends a post request in order to get the next question
- Request Body:

{
    'previous_questions': [1, 4, 20, 15]
    quiz_category': 'current category'
 }

- Returns: a single new question object

{
    'success': True,
    'question': {
        'id': 1,
        'question': 'This is a question',
        'answer': 'This is an answer',
        'difficulty': 5,
        'category': 4
    }
}


#### POST '/questions'

- Sends a post request in order to add a new question
- Request Body:

{
    'question':  'Heres a new question string',
    'answer':  'Heres a new answer string',
    'difficulty': 1,
    'category': 3,
}

- Returns: 
{
    'success': True
}


#### POST '/questions/search'

- Sends a post request in order to search for a specific question by search term
- Request Body:

{
    'searchTerm': 'this is the term the user is looking for'
}

- Returns: any array of questions, a number of totalQuestions that met the search term and the current category string

{
    'success': True,
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer',
            'difficulty': 5,
            'category': 5
        },
    ],
    'totalQuestions': 100,
    'currentCategory': 'Entertainment'
}

## Authors
- Abdullahi Kawu
- Sudhanshu Kulshrestha
- Sarah Maris

## Acknowledgements
I give thanks to ALX, Udacity for opportunity to be a part of the program and course instructor, Caryn McCarthy, for making the course easy to apprenend.
