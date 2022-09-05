import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10
CATEGORIES_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

def paginate_categories(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * CATEGORIES_PER_PAGE
    end = start + CATEGORIES_PER_PAGE

    categories = [categorie.format() for categorie in selection]
    current_categories = categories[start:end]

    return current_categories

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app , resources={r"/api/*": {"origins": "*"}})
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        if request.method == 'OPTIONS':
            response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
            headers = request.headers.get('Access-Control-Request-Headers')
            if headers:
                response.headers['Access-Control-Allow-Headers'] = headers
        return response
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def retrieve_categories():
        selection_all_categories = Category.query.order_by(Category.id).all()
        current_categories = paginate_categories(request, selection_all_categories)
        if current_categories:
            try:
                return jsonify({
                    'success': True,
                    'categories': current_categories,
                    'total_categories': len(selection_all_categories),
                    'categories': {category.id: category.type for category in selection_all_categories}
                })
            except:
                abort(400)
        else:
            abort(404)
            
    # The specific search for the category of the question for fun only
    @app.route('/categories/<int:categorie_id>')
    def get_specific_categorie(categorie_id):
        selection_specific_category_by_id=Category.query.filter_by(id=categorie_id).one_or_none()
        if selection_specific_category_by_id:
            try:
                categorySearchById = Category.query.filter_by(id=str(categorie_id)).all()
                current_categories = paginate_categories(request,categorySearchById)
                return jsonify({
                    'success': True,
                    'categorie': current_categories,
                    'total_category_find': len(current_categories),
                    'category_search_by_id': selection_specific_category_by_id.type
                })
            except:
                abort(400)
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
    @app.route('/questions')
    def retrieve_questions():
        selection= Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)
        if current_questions:
            categories = Category.query.order_by(Category.id).all()
            categoriesSelect = {}
            for category in categories:
                categoriesSelect[category.id] = category.type
            try:
                return jsonify({
                    'success': True,
                    'questions': current_questions,
                    'total_questions': len(selection),
                    'categories': categoriesSelect
                })
            except:
                abort(400)
        else:
            abort(404)
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question_by_id(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            # It is always a good idea to include relevant information in the response so that the correct and
            # expected behaviour of the code can be verified.
            return jsonify({
                'success': True,
                'deleted': question_id,
                'questions': current_questions,
                'total_questions': len(Question.query.all())
            })

        except:
            abort(422)

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
    def new_question_create_question():
        data = request.get_json()

        question = data.get('question', None)
        answer = data.get('answer', None)
        category = data.get('category', None)
        difficulty = data.get('difficulty', None)

        try:
                if not data['answer'] and not data['question'] and not data['category'] and not data['difficulty']:
                    abort(400)
                question = Question(
                    question=question, answer=answer, category=category, difficulty=difficulty)
                question.insert()

                # send back the current questions, to update front end
                selection = Question.query.order_by(Question.id).all()
                currentQuestions = paginate_questions(request, selection)

                return jsonify({
                    'success': True,
                    'question_id': question.id,
                    'questions': currentQuestions,
                    'total_questions': len(selection)
                }), 201
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
    @app.route('/questions/searchTerm', methods=['POST'])
    def get_questions_on_a_search_term():
        body = request.get_json()

        searchTerm = body.get('searchTerm', None)

        if searchTerm:
                questions = Question.query.order_by(Question.id).filter(
                    Question.question.ilike('%{}%'.format(searchTerm)))
                current_quizzes = paginate_questions(request, questions)

                return jsonify({
                    'success': True,
                    'questions': current_quizzes,
                    'total_questions': len(questions.all()),
                    'current_category': None
                })
        else:
            abort(404)
    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def retrieve_questions_based_on_category(category_id):
        selection_retrieve_question_by_category = Category.query.filter_by(id=category_id).one_or_none()
        if selection_retrieve_question_by_category:
            try:
                questionsByCat = Question.query.filter_by(category=str(category_id)).all()
                current_questions = paginate_questions(request,questionsByCat )
                return jsonify({
                    'success': True,
                    'questions': current_questions,
                    'total_questions': len(questionsByCat),
                    'current_category': selection_retrieve_question_by_category.type
                })
            except:
                abort(400)
        else:
            abort(404)
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
    def questions_to_play_the_quiz():
        try:
            body = request.get_json()

            category = body.get('quiz_category', None)
            previous_questions = body.get('previous_questions', None)

            if category['id'] == 0:
                available_questions = Question.query.filter(Question.id.notin_(previous_questions)).all()
            else:
                available_questions = Question.query.filter(Question.category == str(category['id'])).filter(Question.id.notin_(previous_questions)).all()
            if len(available_questions) > 0:
                new_question = available_questions[random.randrange(0, len(available_questions))].format()
            else:
                new_question = None

            return jsonify({
                'success': True,
                'question': new_question
            })
        except:
            abort(422)
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

    @app.errorhandler(405)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 405, "message": "method not allowed"}),
            405,
        )
    @app.errorhandler(500)
    def not_allowed(error):
        return (jsonify({'success': False,'error': 500,'message': 'Internal server error'}), 
            500,
        )

    # The creation of a new category in our TRIVIA API
    @app.route('/categories', methods=['POST'])
    def new_category_create():
        data = request.get_json()
        type = data.get('type', None)
        try:
                if not data['type']:
                    abort(400)
                type = Category(
                    type=type)
                type.insert()

                return jsonify({
                    'success': True,
                    'type_id': type.id,
                    'categories': data,
                }), 201
        except:
            abort(422)

    return app

