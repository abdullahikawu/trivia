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
        self.database_path = "postgresql://{}/{}".format('postgres:0000@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        self.new_question = {
            'question': "Hello", 
            'answer': "Hi", 
            'difficulty': 5,
            'category': 5
        }
        self.questionId = None

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        Question.query.filter(
            Question.question==self.new_question['question'],
            Question.answer==self.new_question['answer']
        ).delete()


    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_200_for_question(self):
        res = self.client().get("/questions/")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])


    def test_404_for_question_invalid_page(self):

        res = self.client().get("/questions/?page=1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Request not found")

    def test_200_for_new_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
    
    def test_400_for_invalid_new_question(self):
        res = self.client().post('/questions', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Invalid request")
    
    def test_200_for_delete_question(self):
        question = Question(**self.new_question)
        question.insert()
        res = self.client().delete('/questions/{}'.format(question.id))
        data = json.loads(res.data)
        self.questionId = question.id

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
    
    def test_404_for_delete_question(self):
        res = self.client().delete('/questions/{}'.format(1000))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Request not found")

    def test_200_for_categories(self):
        res = self.client().get("/categories/")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data['categories'])

    def test_200_for_questions_by_category(self):
        res = self.client().get("/categories/{}/questions".format(3))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], "Geography")

    def test_404_for_questions_by_category(self):
        res = self.client().get("/categories/{}/questions".format(1000))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])

    def test_200_for_search(self):
        res = self.client().post("/questions/search", json={'searchTerm': 'what'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
    
    def test_400_for_invalid_search_term(self):
        res = self.client().post("/questions/search", json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Invalid request")
    
    def test_404_for_search_not_found(self):
        res = self.client().post("/questions/search", json={'searchTerm': 'aehuibfled'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Request not found")
    
    def test_200_for_quizzes(self):
        quizCategory = {"id": 1, "type":"Science"}
        res = self.client().post("/quizzes", json={
            "previous_questions": [20, 22], 
            "quiz_category": quizCategory
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['question'].get('id', None), 21)
        self.assertEqual(data['question'].get('category', None), quizCategory['id'])
    
    def test_400_for_invalid_quiz_category(self):
        res = self.client().post("/quizzes", json={
            "previous_questions": [], 
            "quiz_category": None
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Invalid request")

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()