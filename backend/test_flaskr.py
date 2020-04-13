import os
import unittest
import json
import collections
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


def get_current_time(format='%Y-%m-%d %H:%S:%M'):
    return datetime.now().strftime(format)

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""

        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = 'trivia_test'
        self.database_host = 'localhost'
        self.database_port = 5432
        self.database_user = 'dbuser'
        self.database_pass = 'dbuser'
        self.database_path = "postgresql://{}:{}@{}:{}/{}".format(
            self.database_user,
            self.database_pass,
            self.database_host,
            self.database_port,
            self.database_name
        )
        self.db = setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'Which is the largest moon in the Solar System',
            'answer': 'Ganymede',
            'difficulty': 4,
            'category': 1
        }

        self.new_category = {
            'type': 'Astronomy'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    '''
    Test success response for get_categories
    '''
    def test_get_categories_success(self):
        res = self.client().get('/api/v1/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(isinstance(data, collections.Mapping), True)

    '''
    Test success response for get_questions
    '''
    def test_get_questions_success(self):
        res = self.client().get('/api/v1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(isinstance(data['questions'], collections.Iterable), True)
        self.assertEqual(isinstance(data['total_questions'], int), True)
        self.assertEqual(isinstance(data['categories'], collections.Mapping), True)
        self.assertEqual(data['current_category'], None)

    '''
    Test error response for get_questions with invalid page param
    '''
    def test_get_questions_page_error(self):
        page = -1
        res = self.client().get('/api/v1/questions?page={}'.format(page))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'Unprocessable entity')

    '''
    Test error response for get_questions with invalid per_page param
    '''
    def test_get_questions_per_page_error(self):
        per_page = 1000
        res = self.client().get('/api/v1/questions?per_page={}'.format(per_page))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'Unprocessable entity')

    '''
    Test success response for create_question
    '''
    def test_create_question_success(self):
        new_question_data = self.new_question.copy()
        res = self.client().post('/api/v1/questions', json=new_question_data)
        data = json.loads(res.data)
        new_question = Question.query.order_by(Question.id.desc()).first()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(new_question.question, new_question_data['question'])
        self.assertEqual(new_question.answer, new_question_data['answer'])
        self.assertEqual(new_question.difficulty, new_question_data['difficulty'])
        self.assertEqual(new_question.category, str(new_question_data['category']))

    '''
    Test error response for create_question with invalid question request data
    '''
    def test_create_question_question_error(self):
        new_question_data = self.new_question.copy()
        new_question_data['question'] = ''
        res = self.client().post('/api/v1/questions', json=new_question_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'Unprocessable entity')

    '''
    Test error response for create_question with invalid answer request data
    '''
    def test_create_question_answer_error(self):
        new_question_data = self.new_question.copy()
        new_question_data['answer'] = ''
        res = self.client().post('/api/v1/questions', json=new_question_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'Unprocessable entity')

    '''
    Test error response for create_question with invalid difficulty request data
    '''
    def test_create_question_difficulty_error(self):
        new_question_data = self.new_question.copy()
        new_question_data['difficulty'] = None
        res = self.client().post('/api/v1/questions', json=new_question_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'Unprocessable entity')

    '''
    Test error response for create_question with invalid category request data
    '''
    def test_create_question_category_error(self):
        new_question_data = self.new_question.copy()
        new_question_data['category'] = None
        res = self.client().post('/api/v1/questions', json=new_question_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'Unprocessable entity')

    '''
    Test success response for delete_question
    '''
    def test_delete_question_success(self):
        question = Question.query.order_by(Question.id.desc()).first()
        question_id = question.id
        res = self.client().delete('/api/v1/questions/{}'.format(question_id))
        data = json.loads(res.data)
        question = Question.query.get(question_id)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNone(question)

    '''
    Test error response for delete_question with invalid question_id path variable
    '''
    def test_delete_question_error(self):
        question_id = -1
        res = self.client().delete('/api/v1/questions{}'.format(question_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Not found')

    '''
    Test success response for search_questions
    '''
    def test_search_questions_success(self):
        new_question = self.new_question.copy()
        question = Question(
            question=get_current_time(),
            answer=new_question['answer'],
            difficulty=new_question['difficulty'],
            category=new_question['category']
        )
        question.insert()

        request_body = {
            'search_term': question.question
        }
        res = self.client().post('/api/v1/questions/searches', json=request_body)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(isinstance(data['questions'], collections.Iterable), True)
        self.assertEqual(data['total_questions'], 1)

    '''
    Test success empty response for search_questions
    '''
    def test_search_questions_success_empty_results(self):
        request_body = {
            'search_term': 'jdklaj lksdjlka jksljd lkajlskjdl jasd j1k2j3n4m1n25b41234 daksjdj123'
        }
        res = self.client().post('/api/v1/questions/searches', json=request_body)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 0)
        self.assertEqual(data['total_questions'], 0)

    '''
    Test success response for get_category_questions
    '''
    def test_get_category_questions(self):
        new_category = self.new_category.copy()
        new_question = self.new_question.copy()
        category = Category(type=new_category['type'])
        category.insert()
        question = Question(
            question=new_question['question'],
            answer=new_question['answer'],
            difficulty=new_question['difficulty'],
            category=str(category.id)
        )
        question.insert()

        category_questions = Question.query.filter_by(category=str(category.id)).all()
        res = self.client().get('/api/v1/categories/{}/questions'.format(category.id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(isinstance(data['questions'], collections.Iterable), True)
        self.assertEqual(data['total_questions'], len(category_questions))

    '''
    Test error response for get_category_questions
    '''
    def test_get_category_questions_error(self):
        category_id = 3123124
        res = self.client().get('/api/v1/categories/{}/questions'.format(category_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'Unprocessable entity')

    '''
    Test success response for play_quiz without quiz_category request data
    '''
    def test_play_quiz(self):
        request_body = {
            'previous_questions': []
        }
        res = self.client().post('/api/v1/quizzes', json=request_body)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(isinstance(data['question']['id'], int), True)

    '''
    Test success response for play_quiz with quiz_category request data
    '''
    def test_play_quiz_from_category(self):
        category = Category.query.first()
        request_body = {
            'previous_questions': [],
            'quiz_category': category.format()
        }
        res = self.client().post('/api/v1/quizzes', json=request_body)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['question']['category'], str(category.id))

    '''
    Test error response for play_quiz with missing request body
    '''
    def test_play_quiz_body_error(self):
        res = self.client().post('/api/v1/quizzes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'Unprocessable entity')

    '''
    Test error response for play_quiz with missing previous_questions request data
    '''
    def test_play_quiz_previous_questions_error(self):
        category = Category.query.first()
        request_body = {
            'quiz_category': category.format()
        }
        res = self.client().post('/api/v1/quizzes', json=request_body)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'Unprocessable entity')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
