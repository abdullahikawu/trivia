import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_from(request):
    return (request.args.get('page', 1, type=int) - 1) * QUESTIONS_PER_PAGE

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    
    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r'*': {'origins': '*'}})
    

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorisation')
        response.headers.add('Access-Contrl-Allow-Methods', 'POST, GET, DELETE, PATCH, OPTIONS')
        return response
    
    
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories/')
    def categories():
        categories = {}
        
        for category in Category.query.all():
            categories.update(category.format())
        
        if categories:
            return jsonify({
                'success': True, 
                'categories': categories
            })
        else:
            abort(404)


    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions/')
    def questions():
        categories = {}
        start = paginate_from(request)
        end = start + QUESTIONS_PER_PAGE
        
        questions = Question.query.offset(start).limit(end).all()
        
        # merge formated  category records (dicionary) together
        for category in Category.query.all():
            categories.update(category.format())
        
        # return if question exist for the required page (start offset) 
        if categories and Question.query.count() >= start:
            return jsonify({
                'success': True,
                'questions': [question.format() for question in questions],
                'total_questions': len(questions),
                'categories': categories,
                'current_category': None,
            })
        else:
            abort(404)
    
    
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        
        question = Question.query.filter(Question.id==id).one_or_none()
        if question == None:
            abort(404)
        
        try:
            question.delete() 
        except:
            abort(422)
        
        return jsonify({
            'success': True,
        })

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def add_questions():
        
        data = request.get_json()
        data = {
            'question': data.get("question", None), 
            'answer': data.get("answer", None), 
            'difficulty': data.get("difficulty", None),
            'category': data.get("category", None)
        }
        # abort on any missing request body value
        for key in data.keys():
            if data[key] == None:
                abort(400)
        
        try:
            question = Question(**data)
            question.insert()

            return jsonify({
                'success': True
            })
        except:
            abort(422)

    

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        #{ searchTerm: searchTerm }
        searchTerm = request.get_json().get('searchTerm', None)
        if searchTerm == None:
            abort(400)
        
        questions = Question.query.filter(Question.question.ilike('%{}%'.format(searchTerm))).all()
        
        if len(questions) == 0:
            abort(404)
        
        return jsonify({
            'success': True,
            'questions': [question.format() for question in questions],
            'total_questions': len(questions),
            'current_category': None,
        })



    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    
    @app.route('/categories/<int:id>/questions')
    def questions_by_category(id):
        questions = Question.query.filter(Question.category==id).all()
        
        if len(questions) == 0:
            abort(404)
        
        current_category = Category.query.filter(Category.id==id).one_or_none()
        return jsonify({
            'success': True,
            'questions': [question.format() for question in questions],
            'total_questions': len(questions),
            'current_category': current_category.type
        })

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def next_question():
       
        data = request.get_json()
        
        previousQuestions = data.get("previous_questions", [])
        quizCategory = data.get("quiz_category", None)
        
        # find question not in previousQuestions list
        question = Question.query.filter(~Question.id.in_(previousQuestions))
        
        # filter question by category
        if quizCategory == None:
            abort(400)
        
        categoryId = quizCategory['id']
        question = question.filter(Question.category==categoryId)
        
        # retrieve a question database
        question = question.limit(1).one_or_none()
        if question:
            question = question.format()
        return jsonify({'success': True, 'question': question})
        
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(400)
    def invalid_request(error):
        return jsonify({
            "success": False, 
            "error": 400,
            "message": "Invalid request"
        }), 400
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False, 
            "error": 404,
            "message": "Request not found"
        }), 404

    @app.errorhandler(422)
    def unprocessed_request(error):
        return jsonify({
            "success": False, 
            "error": 422,
            "message": "Something went wrong"
        }), 422
    
    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False, 
            "error": 500,
            "message": "Server error"
        }), 500
    
    return app
