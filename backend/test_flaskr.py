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
        self.database_path = os.getenv("DATABASE_TEST_URI")
        setup_db(self.app, self.database_path)

        self.new_question = {
            "question": "What is my name?",
            "answer": "Jamie",
            "difficulty": "5",
            "category": "4",
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

    def test_get_all_categories(self):
        """Test GET route for retrieving all of the trivia categories"""
        response = self.client().get("/categories")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])
        self.assertTrue(len(data["categories"]))

    def test_405_get_categories_wrong_method(self):
        response = self.client().post("/categories")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")

    def test_get_questions(self):
        response = self.client().get("/questions")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["categories"]))
        self.assertTrue(len(data["questions"]))

    def test_405_get_questions_wrong_method(self):
        response = self.client().patch("/questions")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")

    def test_get_questions_per_category(self):
        response = self.client().get("/categories/4/questions")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["totalQuestions"])
        self.assertTrue(data["currentCategory"])
        self.assertTrue(len(data["questions"]))

    def test_404_if_no_category(self):
        response = self.client().get("/categories/1000/questions")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_quizzes(self):
        response = self.client().post(
            "/quizzes",
            json={
                "previous_questions": ["12", "23"],
                "quiz_category": {"type": "History", "id": "3"},
            },
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])

    def test_405_quizzes_wrong_method(self):
        response = self.client().get("/quizzes")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")

    def test_create_new_question(self):
        response = self.client().post("/questions", json=self.new_question)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(data["total_questions"])

    def test_400_empty_create_new_question(self):
        response = self.client().post("/questions", json={"difficulty": 5})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")

    def test_delete_question_by_id(self):
        response = self.client().delete("/questions/14")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], 14)

    def test_422_if_no_question_to_delete(self):
        response = self.client().delete("/categories/3/questions/1000")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_search_questions(self):
        response = self.client().post(
            "/questions/search", json={"searchTerm": "count"}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["totalQuestions"])

    def test_422_if_no_search_page(self):
        response = self.client().post(
            "/questions/search?page=1000", json={"searchTerm": ""}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
