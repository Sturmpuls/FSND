import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app)

    @app.after_request
    def after_request(response):
        '''Specifies allowed origins, headers and HTTP methods.
        '''

        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, PUT, POST, PATCH, DELETE, OPTIONS')

        return response

    @app.route('/categories', methods=['GET'])
    def get_categories():
        '''Handles GET requests for querying available categories.
        '''

        # get all categories and convert them to a dict like so {id: category}
        selection = Category.query.all()
        categories = {category.id: category.type for category in selection}

        # abort with 404 if no categories were found
        if len(categories) == 0:
            abort(404)

        # return the results
        return jsonify({
            'success': True,
            'categories': categories
        })

    @app.route('/questions', methods=['GET'])
    def get_questions():
        '''Handles GET requests for questions. Results are paginated.

        Parameters
        ----------
        pages : `int`
            Page number to display. A page usually contains 10 questions.

        Returns
        -------
        json
            a dict containing question objects for the queried page
            as well as some other attributes
        '''

        # get all questions and paginate
        selection = Question.query.all()
        total_questions = len(selection)
        current_questions = paginate_questions(request, selection)

        # get all categories and add to dict like {id: category}
        categories = {category.id: category.type for category in selection}

        # return 404 if the requested page exceeded the available questions
        if len(current_questions) == 0:
            abort(404)

        # return the result as json
        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': total_questions,
            'current_category': None,
            'categories': categories
        })

    '''
    @DONE:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    '''
    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        question = Question.query.get(id)

        # abort with 404 if no question is found
        if question is None:
            abort(404)

        question.delete()

        return jsonify({
            'success': True,
            'deleted': id
        })

    '''
    @DONE:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    '''
    @app.route('/questions', methods=['POST'])
    def add_question(question, answer, category, difficulty):
        body = request.get_data()

        if ('question' in body and 'answer' in body and
            'category' in body and 'difficulty' in body):

            new_question = body.get('question')
            new_answer = body.get('answer')
            new_category = body.get('category')
            new_difficulty = body.get('difficulty')

            try:
                question = Question(question=new_question, answer=new_answer,
                                    category=new_category, difficulty=new_difficulty)
                question.insert()

                return jsonify({
                    'success': True,
                    'created': question.id
                })

            except:
                abort(422)

        else:
            abort(422)



    '''
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''

    '''
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''

    '''
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    '''

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    return app
