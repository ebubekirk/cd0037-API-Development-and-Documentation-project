import os
import unittest

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
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    
    def testGetQuestions(self):
        """Test getting all questions"""
        res = self.client().get('/questions')
        
        self.assertEqual(res.status_code,200)
    
    def testGetRequests(self):
        """Test getting all requests"""
        res = self.client().get('/requests')
        
        self.assertEqual(res.status_code,200)
    
    def testDeleteQuestion(self):
        """Test deleting a question with id"""
        res = self.client().delete('/questions')
        
        self.assertEqual(res.status_code,200)
    
    def testCreateQuestion(self):
        """Test creating a question"""
        res = self.client().post('/questions')
        
        self.assertEqual(res.status_code,200)
    
    def testGetQuestionCategory(self):
        """Test getting questions by category"""
        res = self.client().post('/questions')
        
        self.assertEqual(res.status_code,200)
    
    def testGetQuestionSearch(self):
        """Test getting questions with search term"""
        res = self.client().post('/questions')
        
        self.assertEqual(res.status_code,200)
    
    def testGetQuizQuestions(self):
        """Test getting quiz questions"""
        res = self.client().get('/questions')
        
        self.assertEqual(res.status_code,200)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
