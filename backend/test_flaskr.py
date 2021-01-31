import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432',
                                                         self.database_name)

        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'Who was president of the USA in 2019?',
            'answer': 'Donald Trump',
            'category': 4,
            'difficulty': 1,
        }

        self.empty_question = {
            'question': '',
            'answer': 'This should not be possible',
            'category': 1,
            'difficulty': 1,
        }

        self.search_question = {
            'searchTerm': 'penicillin'
        }

        self.search_question_not_found = {
            'searchTerm': 'xyzabcdefg000notfound'
        }

        self.random_question = {
            'previous_questions': [],
            'quiz_category': {'id': 0}
        }

        self.bad_random_question = {
            'previous_questions': []
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after each test"""
        pass

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories_total'])
        self.assertTrue(len(data['categories']))

    def test_get_questions_by_category(self):
        cat_id = 1
        res = self.client().get(f'/categories/{cat_id}/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['current_category'], cat_id)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], None)
        self.assertTrue(len(data['categories']))

    def test_add_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        new_question = Question.query.order_by(Question.id.desc()).first()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertEqual(data['created'], new_question.id)
        self.assertEqual(self.new_question['question'], new_question.question)
        self.assertEqual(self.new_question['answer'], new_question.answer)
        self.assertEqual(self.new_question['difficulty'],
                         new_question.difficulty)
        self.assertEqual(self.new_question['category'], new_question.category)

    def test_delete_question(self):
        id = Question.query.first().id
        res = self.client().delete(f'/questions/{id}')
        data = json.loads(res.data)

        query_deleted = Question.query.filter_by(id=id).first()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], id)
        self.assertIsNone(query_deleted)

    def test_search_question(self):
        res = self.client().post('/questions', json=self.search_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])

    def test_get_random_question(self):
        res = self.client().post('/quizzes', json=self.random_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['question'])

    def test_400_if_random_question_bad_format(self):
        res = self.client().post('/quizzes', json=self.bad_random_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'bad request')

    def test_404_if_get_questions_none(self):
        res = self.client().get('/questions?page=10000000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'resource not found')

    def test_404_if_get_questions_by_category_none(self):
        res = self.client().get('/categories/1/questions?page=10000000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'resource not found')

    def test_404_if_delete_question_not_found(self):
        id = -1
        res = self.client().delete(f'/questions/{id}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'resource not found')

    def test_404_if_search_question_not_found(self):
        res = self.client().post('/questions',
                                 json=self.search_question_not_found)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'resource not found')

    def test_422_if_add_question_empty(self):
        res = self.client().post('/questions', json=self.empty_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'unprocessable')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
