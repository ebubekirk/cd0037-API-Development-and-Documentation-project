import os
import unittest
import json

from flaskr import create_app
from models import db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_name = os.getenv("DB_NAME_TEST", "trivia_test")
        self.database_user = os.getenv("DB_USER", "postgres")
        self.database_password = os.getenv("DB_PASSWORD", "password")
        self.database_host = os.getenv("DB_HOST", "localhost")
        self.database_port = os.getenv("DB_PORT", "5432")
        self.database_path = f"postgresql://{self.database_user}:{self.database_password}@{self.database_host}:{self.database_port}/{self.database_name}"

        # Create app with the test configuration
        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": self.database_path,
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "TESTING": True
        })
        self.client = self.app.test_client()

        # Bind the app to the current context and create all tables
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """Executed after each test"""
        pass
        #with self.app.app_context():
        #    db.session.remove()
        #    db.drop_all()

    # ========== GET /categories Tests ==========
    def test_get_categories_success(self):
        """Test getting all categories successfully"""
        res = self.client.get('/categories')
        
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertIn('categories', data)
        self.assertIn('total_categories', data)
        self.assertEqual(data['total_categories'], 6)

    # ========== GET /questions Tests ==========
    def test_get_questions_success(self):
        """Test getting all questions successfully"""
        res = self.client.get('/questions')
        
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertIn('questions', data)
        self.assertIn('total_questions', data)
        self.assertIn('categories', data)
        self.assertEqual(data['total_questions'], 19)
        self.assertEqual(len(data['questions']), 10)

    def test_get_questions_beyond_pagination(self):
        """Test getting questions beyond pagination"""

        res = self.client.get('/questions?page=999')
        
        self.assertEqual(res.status_code, 404)
        data = json.loads(res.data)
        self.assertFalse(data['success'])

    def test_get_questions_page_2(self):
        """Test getting questions on page 2"""

        res = self.client.get('/questions?page=2')
        
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['questions']), 9)

    # ========== DELETE /questions/<id> Tests ==========
    def test_delete_question_success(self):
        """Test deleting a question successfully"""
        with self.app.app_context():
            question = db.session.query(Question).all()[0]
            question_id = question.id

        res = self.client.delete(f'/questions/{question_id}')
        
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], question_id)

    def test_delete_question_not_found(self):
        """Test deleting a question that doesn't exist"""
        res = self.client.delete('/questions/99999')
        
        self.assertEqual(res.status_code, 404)
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)

    # ========== POST /questions Tests (Create) ==========
    def test_create_question_success(self):
        """Test creating a question successfully"""
        new_question = {
            'question': 'What is 2 + 2?',
            'answer': '4',
            'category': 1,
            'difficulty': 1
        }
        
        res = self.client.post('/questions', 
                              data=json.dumps(new_question),
                              content_type='application/json')
        
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertIn('created', data)
        self.assertIn('questions', data)
        self.assertIn('total_questions', data)

    def test_create_question_missing_question_text(self):
        """Test creating a question with missing question text"""
        incomplete_question = {
            'answer': '4',
            'category': 1,
            'difficulty': 1
        }
        
        res = self.client.post('/questions', 
                              data=json.dumps(incomplete_question),
                              content_type='application/json')
        
        self.assertEqual(res.status_code, 400)
        data = json.loads(res.data)
        self.assertFalse(data['success'])

    def test_create_question_missing_answer(self):
        """Test creating a question with missing answer"""
        incomplete_question = {
            'question': 'What is 2 + 2?',
            'category': 1,
            'difficulty': 1
        }
        
        res = self.client.post('/questions', 
                              data=json.dumps(incomplete_question),
                              content_type='application/json')
        
        self.assertEqual(res.status_code, 400)

    def test_create_question_missing_category(self):
        """Test creating a question with missing category"""
        incomplete_question = {
            'question': 'What is 2 + 2?',
            'answer': '4',
            'difficulty': 1
        }
        
        res = self.client.post('/questions', 
                              data=json.dumps(incomplete_question),
                              content_type='application/json')
        
        self.assertEqual(res.status_code, 400)

    def test_create_question_missing_difficulty(self):
        """Test creating a question with missing difficulty"""
        incomplete_question = {
            'question': 'What is 2 + 2?',
            'answer': '4',
            'category': 1
        }
        
        res = self.client.post('/questions', 
                              data=json.dumps(incomplete_question),
                              content_type='application/json')
        
        self.assertEqual(res.status_code, 400)

    # ========== POST /questions Tests (Search) ==========
    def test_search_questions_success(self):
        """Test searching for questions with a search term"""
        search_query = {
            'searchTerm': 'Africa'
        }
        
        res = self.client.post('/questions', 
                              data=json.dumps(search_query),
                              content_type='application/json')
        
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertIn('questions', data)
        self.assertGreaterEqual(len(data['questions']), 1)
        self.assertEqual(data['total_questions'], len(data['questions']))

    def qtest_search_questions_no_results(self):
        """Test searching for questions with no matching results"""
        search_query = {
            'searchTerm': 'nonexistentterm123456'
        }
        
        res = self.client.post('/questions', 
                              data=json.dumps(search_query),
                              content_type='application/json')
        
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['questions']), 0)
        self.assertEqual(data['total_questions'], 0)

    def qtest_search_questions_case_insensitive(self):
        """Test searching for questions is case insensitive"""
        search_query = {
            'searchTerm': 'CAPITAL'
        }
        
        res = self.client.post('/questions', 
                              data=json.dumps(search_query),
                              content_type='application/json')
        
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertGreaterEqual(len(data['questions']), 1)

    # ========== GET /categories/<id>/questions Tests ==========
    def qtest_get_questions_by_category_success(self):
        """Test getting questions by category successfully"""
        res = self.client.get('/categories/1/questions')
        
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertIn('questions', data)
        self.assertIn('total_questions', data)
        self.assertIn('current_category', data)
        self.assertEqual(data['current_category'], 'Science')
        self.assertEqual(data['total_questions'], 2)

    def qtest_get_questions_by_category_invalid_id(self):
        """Test getting questions for a category that doesn't exist"""
        res = self.client.get('/categories/99999/questions')
        
        self.assertEqual(res.status_code, 404)
        data = json.loads(res.data)
        self.assertFalse(data['success'])

    def qtest_get_questions_by_category_no_questions(self):
        """Test getting questions for a category with no questions"""
        with self.app.app_context():
            category = Category('Empty Category')
            db.session.add(category)
            db.session.commit()
            category_id = category.id

        res = self.client.get(f'/categories/{category_id}/questions')
        
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['questions']), 0)
        self.assertEqual(data['total_questions'], 0)

    # ========== POST /quizzes Tests ==========
    def qtest_play_quiz_success(self):
        """Test getting a quiz question successfully"""
        quiz_data = {
            'quiz_category': {'id': 1, 'type': 'Science'},
            'previous_questions': []
        }
        
        res = self.client.post('/quizzes', 
                              data=json.dumps(quiz_data),
                              content_type='application/json')
        
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertIn('question', data)
        self.assertIsNotNone(data['question'])
        self.assertIn('id', data['question'])

    def qtest_play_quiz_all_categories(self):
        """Test getting a quiz question from all categories"""
        quiz_data = {
            'quiz_category': {'id': 0, 'type': 'click'},
            'previous_questions': []
        }
        
        res = self.client.post('/quizzes', 
                              data=json.dumps(quiz_data),
                              content_type='application/json')
        
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertIsNotNone(data['question'])

    def test_play_quiz_avoid_previous_questions(self):
        """Test that quiz doesn't return previous questions"""
        with self.app.app_context():
            question = db.session.query(Question).first()
            previous_id = question.id

        quiz_data = {
            'quiz_category': {'id': 1, 'type': 'Science'},
            'previous_questions': [previous_id]
        }
        
        res = self.client.post('/quizzes', 
                              data=json.dumps(quiz_data),
                              content_type='application/json')
        
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        
        if data['question'] is not None:
            self.assertNotEqual(data['question']['id'], previous_id)

    def test_play_quiz_all_questions_used(self):
        """Test quiz when all questions have been used"""
        with self.app.app_context():
            questions = db.session.query(Question).all()
            previous_ids = [q.id for q in questions]

        quiz_data = {
            'quiz_category': {'id': 1, 'type': 'Science'},
            'previous_questions': previous_ids
        }
        
        res = self.client.post('/quizzes', 
                              data=json.dumps(quiz_data),
                              content_type='application/json')
        
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertIsNone(data['question'])

    def test_play_quiz_missing_category(self):
        """Test quiz without quiz_category parameter"""
        quiz_data = {
            'previous_questions': []
        }
        
        res = self.client.post('/quizzes', 
                              data=json.dumps(quiz_data),
                              content_type='application/json')
        
        self.assertEqual(res.status_code, 400)
        data = json.loads(res.data)
        self.assertFalse(data['success'])

    # ========== Error Handler Tests ==========
    def test_404_error_handler(self):
        """Test 404 error handler for non-existent endpoint"""
        res = self.client.get('/nonexistent')
        
        self.assertEqual(res.status_code, 404)
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
        self.assertIn('message', data)

    def test_422_error_handler(self):
        """Test 422 error handler"""
        res = self.client.post('/quizzes', 
                              data='invalid json',
                              content_type='application/json')
        
        self.assertIn(res.status_code, [400, 422])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
