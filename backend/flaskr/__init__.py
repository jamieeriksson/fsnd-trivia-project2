import os
import random

from flask import Flask, abort, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from models import Category, Question, setup_db

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET, POST, PATCH, DELETE, OPTIONS"
        )
        response.headers.add("Access-Control-Allow-Credentials", "true")
        return response

    """
    @TODO: 
    Create an endpoint to handle GET requests 
    for all available categories.
    """

    @app.route("/categories")
    def categories():
        try:
            categories = Category.query.order_by(Category.id).all()
            categories = [category.type for category in categories]

            return jsonify(
                {
                    "success": True,
                    "categories": categories,
                    "total_categories": len(categories),
                }
            )
        except:
            abort(400)

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

    @app.route("/questions")
    def questions():
        all_categories = [
            category.type for category in Category.query.order_by(Category.id).all()
        ]
        current_category = Category.query.first()
        all_questions = Question.query.all()

        page = request.args.get("page", 1, type=int)
        current_questions = Question.query.paginate(page, 10, True).items
        formatted_questions = [question.format() for question in current_questions]

        return jsonify(
            {
                "success": True,
                "questions": formatted_questions,
                "totalQuestions": len(all_questions),
                "categories": all_categories,
                "currentCategory": current_category.type,
            }
        )

    """
    @TODO: 
    Create an endpoint to DELETE question using a question ID. 

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    """

    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.filter_by(id=question_id).one_or_none()
            if question is None:
                abort(404)

            question.delete()

            return jsonify({"success": True, "deleted": question_id,})
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

    @app.route("/questions", methods=["POST"])
    def create_questions():
        body = request.get_json()
        print(body)
        new_question = body.get("question", None)
        new_answer = body.get("answer", None)
        new_difficulty = body.get("difficulty", None)

        category_id = body.get("category", None)
        new_category = Category.query.filter_by(id=int(category_id)).first()

        try:
            question = Question(
                question=new_question,
                answer=new_answer,
                difficulty=int(new_difficulty),
                category=str(new_category.id),
            )
            question.insert()

            all_questions = Question.query.all()
            return jsonify(
                {
                    "success": True,
                    "created": question.id,
                    "total_questions": len(all_questions),
                }
            )
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

    @app.route("/questions/search", methods=["POST"])
    def search_questions():
        try:
            body = request.get_json()
            search_term = body.get("searchTerm", None)
            page = request.args.get("page", 1, type=int)

            all_questions = Question.query.filter(
                Question.question.ilike(f"%{search_term}%")
            ).all()

            current_questions = (
                Question.query.filter(Question.question.ilike(f"%{search_term}%"))
                .paginate(page, 10, True)
                .items
            )

            return jsonify(
                {
                    "success": True,
                    "questions": [question.format() for question in current_questions],
                    "totalQuestions": len(all_questions),
                }
            )
        except:
            abort(422)

    """
    @TODO: 
    Create a GET endpoint to get questions based on category. 

    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    """

    @app.route("/categories/<int:category_id>/questions")
    def questions_by_category(category_id):
        category_id += 1
        current_category = Category.query.filter_by(id=category_id).one_or_none()
        if current_category is None:
            abort(404)
        page = request.args.get("page", 1, type=int)
        current_questions = (
            Question.query.filter_by(category=str(category_id))
            .paginate(page, 10, True)
            .items
        )
        all_questions = Question.query.filter_by(category=str(category_id)).all()
        formatted_questions = [question.format() for question in current_questions]
        return jsonify(
            {
                "success": True,
                "questions": formatted_questions,
                "totalQuestions": len(all_questions),
                "currentCategory": current_category.format(),
            }
        )

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

    @app.route("/quizzes", methods=["POST"])
    def quiz():
        body = request.get_json()
        previous_questions = body.get("previous_questions", "")
        quiz_category = body.get("quiz_category")

        if quiz_category["type"] == "click":
            quiz_questions = Question.query.all()
        else:
            quiz_category["id"] = str(int(quiz_category["id"]) + 1)
            quiz_questions = Question.query.filter_by(
                category=quiz_category["id"]
            ).all()

        if len(previous_questions) == len(quiz_questions):
            return jsonify({"question": False})
        else:
            next_question = random.choice(quiz_questions)
            if previous_questions != []:
                while next_question.id in previous_questions:
                    next_question = random.choice(quiz_questions)

            return jsonify({"question": next_question.format()})

    """
    @TODO: 
    Create error handlers for all expected errors 
    including 404 and 422. 
    """

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify({"success": False, "error": 400, "message": "bad request"}),
            400,
        )

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

    return app
