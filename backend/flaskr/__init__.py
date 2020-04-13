from flask import Flask, abort, jsonify, request
from flask_cors import CORS
import random
import collections

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    db = setup_db(app)

    '''
    Set up CORS. Allow '*' for origins.
    '''
    cors = CORS(app, resources={r'/api/*': {'origins': '*'}})

    '''
    Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    '''
    Create an endpoint to handle GET requests 
    for all available categories.
    '''
    @app.route('/api/v1/categories')
    def get_categories():
        try:
            body = {}
            for category in Category.query.all():
                body[category.id] = category.type

            return jsonify({
                'success': True,
                'categories': body
            })
        except:
            abort(404)

    '''
    Create an endpoint to handle GET requests for questions, 
    including pagination (every 10 questions). 
    This endpoint should return a list of questions, 
    number of total questions, current category, categories. 
    
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions. 
    '''
    @app.route('/api/v1/questions')
    def get_questions():
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)

        # page must be larger than zero and per_page must be less or equal to one hundred
        if page < 1 or per_page > 100:
            return abort(422)

        questions_query = Question.query.paginate(page=page, error_out=False, max_per_page=per_page)
        formatted_questions = [question.format() for question in questions_query.items]

        categories = Category.query.all()
        formatted_categories = {}
        for category in categories:
            formatted_categories[category.id] = category.type

        return jsonify({
            'success': True,
            'questions': formatted_questions,
            'total_questions': questions_query.total,
            'categories': formatted_categories,
            'current_category': None
        })

    '''
    Create an endpoint to DELETE question using a question ID.
    
    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    '''
    @app.route('/api/v1/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.filter(Question.id == question_id).one_or_none()

        # question must exist
        if question is None:
            return abort(404)

        question.delete()
        return jsonify({
            'success': True
        })

    '''
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.
    
    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    '''
    @app.route('/api/v1/questions', methods=['POST'])
    def create_question():
        required_request_data = ['question', 'answer', 'difficulty', 'category']
        request_body = request.get_json()

        for key in required_request_data:
            # all required request data must exist
            if key not in request_body or request_body[key] is None or request_body[key] == '':
                return abort(422)

        question = Question(
            request_body['question'],
            request_body['answer'],
            request_body['category'],
            request_body['difficulty']
        )
        question.insert()

        return jsonify({
            'success': True
        })

    '''
    POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 
    '''
    @app.route('/api/v1/questions/searches', methods=['POST'])
    def search_questions():
        request_body = request.get_json()
        search_term = request_body['search_term']
        questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
        formatted_questions = [question.format() for question in questions]

        return jsonify({
            'success': True,
            'questions': formatted_questions,
            'total_questions': len(formatted_questions),
            'current_category': None
        })

    '''
    Create a GET endpoint to get questions based on category. 
    
    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''
    @app.route('/api/v1/categories/<int:category_id>/questions')
    def get_category_questions(category_id):
        category = Category.query.filter(Category.id == category_id).one_or_none()

        # category must exist
        if category is None:
            return abort(422)

        questions = Question.query.filter_by(category=str(category.id)).all()
        formatted_questions = [question.format() for question in questions]

        return jsonify({
            'success': True,
            'questions': formatted_questions,
            'total_questions': len(questions),
            'current_category': category.format()
        })

    '''
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 
    
    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    '''
    @app.route('/api/v1/quizzes', methods=['POST'])
    def play_quiz():
        request_body = request.get_json()

        # request body must exist
        if request_body is None:
            return abort(422)

        # request body must contain 'previous_questions' field with iterable value
        if not ('previous_questions' in request_body) or not isinstance(request_body['previous_questions'], collections.Iterable):
            return abort(422)

        previous_questions = request_body['previous_questions']

        if 'quiz_category' in request_body and not (request_body['quiz_category'] is None):
            quiz_category = request_body['quiz_category']
            not_taken_questions = Question.query.filter(
                Question.category == str(quiz_category['id']),
                Question.id.notin_(previous_questions)
            ).all()
        else:
            not_taken_questions = Question.query.filter(Question.id.notin_(previous_questions)).all()

        random_not_taken_question = random.choice(not_taken_questions)

        return jsonify({
            'success': True,
            'question': random_not_taken_question.format()
        })

    '''
    Create error handlers for all expected errors 
    including 404 and 422. 
    '''
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Not found'
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'Method not allowed'
        }), 405

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable entity'
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal server error'
        }), 500

    return app
