import os
from re import search
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
from settings import DB_NAME1, DB_PASSWORD1, DB_USER1, HOST_NAME1


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name =DB_NAME1
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            DB_USER1, DB_PASSWORD1,HOST_NAME1, self.database_name
        )
        setup_db(self.app, self.database_path)

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
    #block for categories create test unit for page and specific category errors
    def test_get_available_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_get_specific_categorie(self):
        res = self.client().get('/categories/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categorie'])

    def test_get_specific_categorie_not_found_req(self):
        res = self.client().get('/categories/400')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_404_sent_requesting_beyond_valid_page_categorie(self):
        res = self.client().get('/categories?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")
    
    def test_404_sent_requesting_beyond_valid_specific_categorie(self):
        res = self.client().get('/categories/200')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    
    def test_add_category(self):
        newCategory = {
            'type': 'Culture',
        }
        res = self.client().post('/categories', json=newCategory)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(data["success"], True)

    # block for questions create test unit for page and specific question 
    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['questions'])
    
    def test_get_specific_question_method_not_allowed_req(self):
        res = self.client().get('/questions/4')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    def test_404_sent_requesting_beyond_valid_page_question(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/questions?page=1000', json={'difficulty': 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    
    def test_delete_question_specific(self):
        question = Question.query.order_by(self.db.desc(Question.id)).first()
        self.assertNotEqual(question, None)
        question_id =question.id
        res = self.client().delete('/questions/'+str(question_id))
        data = json.loads(res.data)
        question = Question.query.get(question_id)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], question_id)
        self.assertTrue(data['total_questions'])
        self.assertEqual(question, None)
        
    def test_add_question(self):
        newQuestion = {
            'question': 'who is your name?',
            'answer': 'BANYISHAYI',
            'difficulty': 2,
            'category': 1,
        }
        res = self.client().post('/questions', json=newQuestion)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(data["success"], True)

    # Search questions by results by term
    def test_get_question_search_with_results(self):
        res = self.client().post('/questions/searchTerm', json={'searchTerm': 'What'})
        data = json.loads(res.data)
        

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertEqual(len(data['questions']),8)

    def test_get_question_search_without_results(self):
        res = self.client().post('/questions/searchTerm', json={'searchTerm': 'rdcdrdc'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 0)
        self.assertEqual(len(data['questions']), 0)

    #Search questions by question category and error
    def test_questions_in_category_search(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertNotEqual(len(data['questions']), 0)
        self.assertEqual(data['current_category'], 'Science')
    
    def test_questions_in_category_not_found(self):
        res = self.client().get('/categories/100/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    #The test quiz is over
    def test_play_quiz_is_over(self):
        new_quiz = {
            'previous_questions': [2, 4, 6],
            'quiz_category': {'type': 'Entertainment', 'id': 5}
        }
        res = self.client().post('/quizzes', json=new_quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNone(data['question'])

    #Test play a quiz not finish
    def test_play_quiz_not_over(self):
        new_quiz = {
            'previous_questions': [],
            'quiz_category': {'type': 'Culture', 'id': 1}
        }

        res = self.client().post('/quizzes', json=new_quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_422_play_quiz(self):
        new_quiz_round = {'previous_questions': []}
        res = self.client().post('/quizzes', json=new_quiz_round)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()