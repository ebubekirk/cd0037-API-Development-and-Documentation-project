# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## API Endpoints Documentation

### GET '/categories'

Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category.

**Request Arguments:** None

**Returns:** An object with keys:
- `success` (boolean): Indicates if the request was successful
- `categories` (object): Contains an object of `id: category_string` key:value pairs
- `total_categories` (integer): Total number of categories

**Example Response:**
```json
{
  "success": true,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "total_categories": 6
}
```

**Error Response (404 - No categories found):**
```json
{
  "success": false,
  "error": 404,
  "message": "Resource not found"
}
```

---

### GET '/questions'

Fetches a paginated set of questions from the database (10 questions per page).

**Request Arguments:**
- `page` (query parameter, optional): Page number (defaults to 1)

**Returns:** An object with keys:
- `success` (boolean): Indicates if the request was successful
- `questions` (array): List of question objects with id, question, answer, category, and difficulty
- `total_questions` (integer): Total number of questions in the database
- `categories` (object): Dictionary of all available categories
- `current_category` (null): Placeholder for category filtering

**Example Response:**
```json
{
  "success": true,
  "questions": [
    {
      "id": 1,
      "question": "What is the capital of France?",
      "answer": "Paris",
      "category": 4,
      "difficulty": 1
    },
    {
      "id": 2,
      "question": "What is the chemical symbol for gold?",
      "answer": "Au",
      "category": 1,
      "difficulty": 2
    }
  ],
  "total_questions": 20,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History"
  },
  "current_category": null
}
```

**Error Response (404 - No questions found):**
```json
{
  "success": false,
  "error": 404,
  "message": "Resource not found"
}
```

---

### DELETE '/questions/<question_id>'

Deletes a question by its ID from the database.

**Request Arguments:**
- `question_id` (URL parameter, required): The ID of the question to delete

**Returns:** An object with keys:
- `success` (boolean): Indicates if the request was successful
- `deleted` (integer): The ID of the deleted question

**Example Response:**
```json
{
  "success": true,
  "deleted": 5
}
```

**Error Response (404 - Question not found):**
```json
{
  "success": false,
  "error": 404,
  "message": "Resource not found"
}
```

---

### POST '/questions'

Creates a new question in the database. This endpoint handles two operations:
1. Creating a new question (when `searchTerm` is not provided)
2. Searching for questions (when `searchTerm` is provided)

#### 1. Create Question

**Request Body:**
```json
{
  "question": "What is the largest planet in our solar system?",
  "answer": "Jupiter",
  "category": 1,
  "difficulty": 2
}
```

**Returns:** An object with keys:
- `success` (boolean): Indicates if the request was successful
- `created` (integer): The ID of the newly created question
- `questions` (array): Updated list of questions on the last page
- `total_questions` (integer): Total number of questions in the database

**Example Response:**
```json
{
  "success": true,
  "created": 25,
  "questions": [
    {
      "id": 24,
      "question": "Previous question",
      "answer": "Answer",
      "category": 1,
      "difficulty": 1
    },
    {
      "id": 25,
      "question": "What is the largest planet in our solar system?",
      "answer": "Jupiter",
      "category": 1,
      "difficulty": 2
    }
  ],
  "total_questions": 25
}
```

**Error Response (400 - Missing required fields):**
```json
{
  "success": false,
  "error": 400,
  "message": "Bad request"
}
```

#### 2. Search Questions

**Request Body:**
```json
{
  "searchTerm": "what"
}
```

**Returns:** An object with keys:
- `success` (boolean): Indicates if the request was successful
- `questions` (array): List of questions matching the search term
- `total_questions` (integer): Total number of matching questions
- `current_category` (null): Placeholder for category filtering

**Example Response:**
```json
{
  "success": true,
  "questions": [
    {
      "id": 1,
      "question": "What is the capital of France?",
      "answer": "Paris",
      "category": 4,
      "difficulty": 1
    },
    {
      "id": 5,
      "question": "What is the largest planet?",
      "answer": "Jupiter",
      "category": 1,
      "difficulty": 2
    }
  ],
  "total_questions": 2,
  "current_category": null
}
```

**Empty Search Result:**
```json
{
  "success": true,
  "questions": [],
  "total_questions": 0,
  "current_category": null
}
```

---

### GET '/categories/<category_id>/questions'

Fetches all questions for a specific category.

**Request Arguments:**
- `category_id` (URL parameter, required): The ID of the category

**Returns:** An object with keys:
- `success` (boolean): Indicates if the request was successful
- `questions` (array): List of questions in the specified category
- `total_questions` (integer): Total number of questions in the category
- `current_category` (string): The name of the category

**Example Response:**
```json
{
  "success": true,
  "questions": [
    {
      "id": 1,
      "question": "What is the capital of France?",
      "answer": "Paris",
      "category": 4,
      "difficulty": 1
    },
    {
      "id": 3,
      "question": "What is the largest country in the world?",
      "answer": "Russia",
      "category": 4,
      "difficulty": 2
    }
  ],
  "total_questions": 2,
  "current_category": "History"
}
```

**Error Response (404 - Category not found):**
```json
{
  "success": false,
  "error": 404,
  "message": "Resource not found"
}
```

---

### POST '/quizzes'

Fetches a random question to play the quiz game. The endpoint can filter by category and exclude previously asked questions.

**Request Body:**
```json
{
  "quiz_category": {
    "id": 1,
    "type": "Science"
  },
  "previous_questions": [1, 2, 5]
}
```

**Query Parameters:**
- `quiz_category` (required): An object with `id` (0 for all categories) and `type` (category name)
- `previous_questions` (optional): Array of question IDs already asked in this quiz session

**Returns:** An object with keys:
- `success` (boolean): Indicates if the request was successful
- `question` (object|null): A random question object, or null if no questions remain

**Example Response (Question Found):**
```json
{
  "success": true,
  "question": {
    "id": 10,
    "question": "What is the chemical symbol for gold?",
    "answer": "Au",
    "category": 1,
    "difficulty": 2
  }
}
```

**Example Response (All Questions Used):**
```json
{
  "success": true,
  "question": null
}
```

**Example Request (All Categories):**
```json
{
  "quiz_category": {
    "id": 0,
    "type": "click"
  },
  "previous_questions": []
}
```

**Error Response (400 - Missing quiz_category):**
```json
{
  "success": false,
  "error": 400,
  "message": "Bad request"
}
```

---

## Error Handlers

### 400 - Bad Request
Returned when the request is malformed or required parameters are missing.

```json
{
  "success": false,
  "error": 400,
  "message": "Bad request"
}
```

### 404 - Not Found
Returned when the requested resource does not exist.

```json
{
  "success": false,
  "error": 404,
  "message": "Resource not found"
}
```

### 422 - Unprocessable Entity
Returned when the request is well-formed but cannot be processed.

```json
{
  "success": false,
  "error": 422,
  "message": "Unprocessable entity"
}
```

### 500 - Internal Server Error
Returned when an unexpected server error occurs.

```json
{
  "success": false,
  "error": 500,
  "message": "Internal server error"
}
```

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

