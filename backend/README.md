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

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

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
flask run
```

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

## Endpoints

GET '/categories',  
GET '/questions',  
DELETE '/questions/int:question_id',  
POST '/questions',  
POST '/questions/search',  
GET '/categories/int:category_id/questions',  
POST '/quizzes'

GET '/categories'

- Fetches a list of the question categories.
- Request Arguments: None
- Returns: An object with the total number of categories and a list containing all of the category types.
  ```
  {'categories' :
    [ "Science",
      "Art",
      "Geography",
      "History",
      "Entertainment",
      "Sports"],
  'total_categories': 6}
  ```

GET '/questions'

- Fetches a list of dictionaries containing the question, answer, difficulty, and category of all the questions in the trivia db. Questions are paginated to return 10 questions per page.
- Request Arguments: None
- Returns: An object with a list of the paginated questions, the total number of questions, and a list of all of the question categories types.
  ```
  {'questions': [
    {
      "answer": "Maya Angelou",
      "category": "4",
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Muhammad Ali",
      "category": "4",
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    }, ...
  ],
  'totalQuestions': 18,
  'categories': [
    "Science",
    "Art",
    "Geography",
    "History",
    "Entertainment",
    "Sports"
  ]}
  ```

DELETE '/questions/int:question_id'

- Deletes a question by question ID.
- Request Arguments: question_id (Integer)
- Returns: An object with the id of the question that was deleted
  ```
  {'deleted': 14}
  ```

POST '/questions'

- Posts a new question to the db.
- Request Arguments: question, answer, difficulty, category
- Returns: An object with the id of the newly created question and the new current total number of questions

  ```
    {'created': 23, 'total_questions': 17}
  ```

POST '/questions/search'

- Fetches questions that match a given search term. The search is case insensitive.
- Request Arguments: searchTerm
- Returns: An object containing a list of dictionaries of the questions with keys for the id, question, answer, difficulty, and category which matched the search term and the total number of questions which matched.
  ```
  {'questions': [
    {
    "answer": "The Palace of Versailles",
    "category": "3",
    "difficulty": 3,
    "id": 14,
    "question": "In which royal palace would you find the Hall of Mirrors?"
    }],
  'totalQuestions': 1}
  ```

GET '/categories/int:category_id/questions'

- Fetches all of the questions within the category of the given category ID.
- Request Arguments: category_id
- Returns: An object containing a list of dictionaries of the questions in the given category with keys for the id, question, answer, difficulty, and category of each question; the total number of questions in that category; and a dictionary of the current category with keys of the id and type of the category.

  ```
  {
  "currentCategory": {
    "id": 3,
    "type": "Geography"
    },
  "questions": [
    {
      "answer": "Lake Victoria",
      "category": "3",
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": "3",
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "totalQuestions": 2
  }
  ```

POST '/quizzes'

- Fetches a random, unanswered question from the given category until there are no more remaining questions.
- Request Arguments: previous_questions (a list of previously asked question IDs), quiz_category (a dictionary with keys for the ID and type of the quiz category)
- Returns: An object containing a dictionary of a random unasked question within the given category. The dictionary has keys for the id, question, answer, difficulty, and category of the question. If all questions have been asked an object with the key question and the value of False is returned.

  ```
  {'question': {
    "answer": "Jackson Pollock",
    "category": "2",
    "difficulty": 2,
    "id": 19,
    "question": "Which American artist was a pioneer of Abstract  Expressionism,   and a leading exponent of action painting?"
  }}
  ```

  or

  ```
  {'question': False}
  ```

## Testing

To run the tests, run

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
