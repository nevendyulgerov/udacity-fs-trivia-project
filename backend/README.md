# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run --host='0.0.0.0' --port=8000
```

This will make the server api discoverable at http://localhost:8000/api/v1.

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

API Endpoints
```
GET '/api/v1/categories'
GET '/api/v1/questions'
POST '/api/v1/questions/searches'
POST '/api/v1/questions'
DELETE '/api/v1/questions/{id}'
GET '/api/v1/categories/{id}/questions'
POST '/api/v1/quizzes'
```

```
GET '/api/v1/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}
```

```
GET '/api/v1/questions?page={page}&per_page={per_page}'
- Fetches paginated questions. Default pagination is 10 questions per page.
- Request Arguments:
    - page: determines the current page value (int) (optional, default=1)
    - per_page: determines the current per page value (int) (optional, default=10)
- Returns the success status, a list of questions, number of total questions, current category, categories.
{
    'success': success status (bool),
    'questions': list of questions (collection.Iterable),
    'total_questions': number of total questions (int),
    'categories': formatted_categories (collection.Mappable),
    'current_category': the current category (collection.Mappable | None)
}
```

```
POST '/api/v1/questions/searches?search_term={search_term}'
- Fetches questions based on a search term.
- Request Arguments:
    - search_term: determines the search term (str) (optional, default='')
- Returns the success status, any questions for whom the search term is a substring of the question, number of total questions, current category
{
    'success': success status (bool),
    'questions': list of questions (collection.Iterable),
    'total_questions': number of total questions (int),
    'current_category': the current category (collection.Mappable | None)
}
```

```
POST '/api/v1/questions'
- Creates a new question with required attributes for question, answer, difficulty, category
- Request Body:
    - question: the question (str) (required)
    - answer: the answer (str) (required)
    - difficulty: the difficulty (int) (required)
    - category: the category (int) (required)
- Returns the success status of the insert question action
{
    'success': success status (bool),
}
```

```
DELETE '/api/v1/questions/{id}'
- Deletes an existing question from the db
- Path Variables:
    - id: the question id (int) (required)
- Returns the success status of the delete question action
{
    'success': success status (bool),
}
```

```
GET '/api/v1/categories/{id}/questions'
- Fetches questions that belong to a specific category.
- Path Variables:
    - id: the category id (int) (required)
- Returns the success status, a list of questions, number of total questions, current category.
{
    'success': success status (bool),
    'questions': list of questions (collection.Iterable),
    'total_questions': number of total questions (int),
    'current_category': the current category (collection.Mappable | None)
}
```

```
POST '/api/v1/quizzes'
- Gets a random question to play the quiz. This endpoint takes category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
- Request Body:
    - quiz_category: the quiz category (int) (optional, default=None)
    - previous_questions: the answer (collection.Iterable) (required)
- Returns the success status of the insert question action and the next random, not already taken question.
{
    'success': success status (bool),
    'question': the next random, not already taken question (collection.Mappable)
}
```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```