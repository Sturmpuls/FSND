# Full Stack API Second Project

## Full Stack Trivia

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a  webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category.

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others.

## Getting started

### Prerequisites

* [Python](https://www.python.org/downloads/) (3.7 or higher)
* [PostgreSQL](https://www.postgresql.org/download/)
* [Node.js](https://nodejs.org/en/download/)

### Installing Dependencies

#### Virtual Environment

The use of a virtual environment is highly recommended. Create a virtual
environment within the `backend` folder.

```
python -m venv c:\path\to\backend\folder\env
```

Activate the virtual environment
* On Windows run `env\Scripts\activate.bat`
* On Linux run `source env/bin/activate`

#### PIP Dependencies

Navigate to the `backend` folder, start the virtual environment and run

```
pip install -r requirements.txt
```

This will install all of the required packages for the app.

#### Key Dependencies

* [Flask](https://flask.palletsprojects.com/en/1.1.x/) is a lightweight microframework for web development in Python.
* [SQLAlchemy](https://www.sqlalchemy.org/) is a SQL Toolkit for Python.
* [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/) is used to handle cross-origin requests from the frontend to
the backend.

### Database Setup

Postgres has to be installed for this. Use the provided `trivia.psql` file to
create a working database for the app.

```
psql trivia < trivia.psql
```

### Running the Server

#### Backend

Activate the previously created virtual environment within the `backend` folder.

On Windows run `env\Scripts\activate.bat`

On Linux run `source env/bin/activate`

To run the server execute:

```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

#### Frontend

In the `frontend` folder execute:

```
npm install  # (only once)
npm start
```

### Testing
Database setup
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
```

Run tests
```
python test_flaskr.py
```

## API Reference

### Getting started
* Base URL: This app can only be run locally. It is hosted at https://localhost:5000/ per default and the frontend is configured accordingly.
* Authentication: This version of the app does not require any kind of authentication.

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    'success': False,
    'error': 400,
    'message': 'bad request'
}
```
The API will return three error types when requests fail:
* 400: bad request
* 404: resource not found
* 422: not processable

### GET /categories

* General:
    * Returns a list of categories, total number of categories and a success value

* Sample: `curl http://localhost:5000/categories`

```
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "categories_total": 6,
    "success": true
}
```

### GET /categories/category_id/questions

* General:
    * Returns a list of questions in the given category, total number of questions
    in the given category, ID of the current category, success value
    * Results are paginated in groups of 10. Page numbers start with 1 and can
    be requested with a `?page=` argument.

* Sample: `curl http://localhost:5000/categories/1/questions?page=1`

```
{
    "current_category": 1,
    "questions": [
        {
            "answer": "The Liver",
            "category": 1,
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?"
        },
        {
            "answer": "Alexander Fleming",
            "category": 1,
            "difficulty": 3,
            "id": 21,
            "question": "Who discovered penicillin?"
        },
        {
            "answer": "Blood",
            "category": 1,
            "difficulty": 4,
            "id": 22,
            "question": "Hematology is a branch of medicine involving the study of what?"
        }
    ],
    "success": true,
    "total_questions": 3
}
```

### GET /questions

* General:
    * Returns a list of questions, total number of questions, ID of the current
    category (should be `null`), list of categories, and a success value
    * Results are paginated in groups of 10. Page numbers start with 1 and can
    be requested with a `?page=` argument.

* Sample: `curl http://localhost:5000/questions?page=1`

```
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "current_category": null,
    "questions": [
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        },
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        {
            "answer": "Brazil",
            "category": 6,
            "difficulty": 3,
            "id": 10,
            "question": "Which is the only team to play in every soccer World Cup tournament?"
        },
        {
            "answer": "Uruguay",
            "category": 6,
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?"
        },
        {
            "answer": "George Washington Carver",
            "category": 4,
            "difficulty": 2,
            "id": 12,
            "question": "Who invented Peanut Butter?"
        },
        {
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
        },
        {
            "answer": "The Palace of Versailles",
            "category": 3,
            "difficulty": 3,
            "id": 14,
            "question": "In which royal palace would you find the Hall of Mirrors?"
        }
    ],
    "success": true,
    "total_questions": 19
    }
```

### POST /questions
* General:
    * Add new question using the submitted question, answer, difficulty,
    and category. All the parameters are required. Returns the created question
    ID and a success value.
    * Return questions containing a given substring if `searchTerm` is specified.
    Returns a list of questions, total number of questions, and a success value.

* Sample: `curl -X POST http://localhost:5000/questions -H "Content-Type: application/json" -d '{"question":"Who was president of the USA in 2020?", "answer":"Donald Trump", "difficulty":1, "category":4}'`

```
{
    "created": 25,
    "success": true
}
```

* Sample: `curl -X POST http://localhost:5000/questions -H "Content-Type: application/json" -d '{"searchTerm":"World Cup"}'`

```
{
    "questions": [
    {
        "answer": "Brazil",
        "category": 6,
        "difficulty": 3,
        "id": 10,
        "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
        "answer": "Uruguay",
        "category": 6,
        "difficulty": 4,
        "id": 11,
        "question": "Which country won the first ever soccer World Cup in 1930?"
    }
    ],
    "success": true,
    "total_questions": 2
}
```

### DELETE /questions/question_id

* General:
    * Deletes the question with the given ID if it exists. Returns the ID of the
    deleted question and a success value

* Sample: `curl -X DELETE http://localhost:5000/questions/2`

```
{
    "deleted": 2,
    "success": true
}
```

### POST /quizzes

* General:
    * Returns a randomly chosen question in the given `quiz_category` (0 for
    all categories) and a success value.
    * If a list of IDs from `previous_questions` is supplied they will be
    excluded from the selection process.
    * If no more questions are left `question` will be returned as `null`.

* Sample: `curl -X POST http://localhost:5000/quizzes -H "Content-Type: application/json" -d '{"quiz_category": {"type":"Science", "id":1}, "previous_questions":[21]}'`

```
{
    "question": {
        "answer": "The Liver",
        "category": 1,
        "difficulty": 4,
        "id": 20,
        "question": "What is the heaviest organ in the human body?"
    },
    "success": true
}
```
