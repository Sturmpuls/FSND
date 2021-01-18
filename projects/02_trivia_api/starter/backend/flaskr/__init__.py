import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

# This variable is also set in the front-end in QuestionView.js
# Function: createPagination()
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
        '''Specify allowed origins, headers and HTTP methods.

        Return a response object.
        '''
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, PUT, POST, PATCH, DELETE, OPTIONS')

        return response

    @app.route('/categories', methods=['GET'])
    def get_categories():
        '''Return available categories.'''
        selection = Category.query.all()
        categories = {category.id: category.type for category in selection}

        if len(categories) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': categories,
            'categories_total': len(categories)
        })

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        '''Get all questions in a category and return paginated questions.'''
        selection = Question.query.filter(
            Question.category == category_id
            ).all()
        current_questions = paginate_questions(request, selection)

        if len(current_questions) == 0:
            return abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(selection),
            'current_category': category_id
        })

    @app.route('/questions', methods=['GET'])
    def get_questions():
        '''Get all questions in all categories and return paginated questions.'''

        # get all questions and paginate
        selection = Question.query.all()
        total_questions = len(selection)
        current_questions = paginate_questions(request, selection)

        # get all categories
        categories = {category.id: category.type
                      for category in Category.query.all()}

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

    @app.route('/questions', methods=['POST'])
    def add_question():
        body = request.get_json()

        # redirect if request contains a search_term
        if 'searchTerm' in body.keys():
            return search_questions(request, body['searchTerm'])

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

    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):

        try:
            question = Question.query.get(id)

            # abort with 404 "Not Found" if no question is found
            if question is None:
                abort(404)

            question.delete()

            return jsonify({
                'success': True,
                'deleted': id
            })

        except:
            # abort with 422 "Unprocessable Entity" if anything else goes wrong
            abort(422)

    def search_questions(request, search_term):
        # query the database and find any substring equaling the search term
        regex = Question.question.ilike(f'%{search_term}%')
        questions = Question.query.filter(regex).all()
        total_questions = len(questions)

        if (total_questions == 0):
            return abort(404)

        current_questions = paginate_questions(request, questions)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': total_questions
        })

    @app.route('/quizzes', methods=['POST'])
    def get_random_question():
        body = request.get_json()

        if body is None or 'quiz_category' not in body.keys():
            return abort(422)

        previous_questions = []
        if 'previous_questions' in body.keys():
            previous_questions = body['previous_questions']

        category = body['quiz_category']['id']
        # "ALL" categories
        if category == 0:
            query = Question.query.filter(
                Question.id.notin_(previous_questions)
                )
        # Specific category
        else:
            query = Question.query.filter(
                Question.category == category,
                Question.id.notin_(previous_questions)
                )
        # Get random question from database
        row_count = int(query.count())
        question = query.offset((int(row_count * random.random()))).first()

        return jsonify({
            'success': True,
            'question': question.format()
        })

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
