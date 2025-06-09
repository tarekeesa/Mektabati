import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models.book import db, Book
from ma_bib import LibraryDataProcessor

class TestMektabatiApp(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
    
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Mektabati', response.data)
    
    def test_add_book_page(self):
        response = self.client.get('/add_book')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Add New Book', response.data)
    
    def test_search_page(self):
        response = self.client.get('/search')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Search Books', response.data)
    
    def test_api_books(self):
        response = self.client.get('/api/books')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')

class TestLibraryDataProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = LibraryDataProcessor()
    
    def test_add_imsi_books(self):
        self.processor.add_sample_imsi_books()
        self.assertEqual(len(self.processor.books_data), 2)
    
    def test_add_personal_books(self):
        self.processor.add_personal_choice_books()
        self.assertEqual(len(self.processor.books_data), 5)
    
    def test_create_dataframe(self):
        self.processor.add_sample_imsi_books()
        self.processor.add_personal_choice_books()
        df = self.processor.create_dataframe()
        self.assertEqual(len(df), 7)
        self.assertIn('title', df.columns)
        self.assertIn('author', df.columns)
    
    def test_search_functionality(self):
        self.processor.add_sample_imsi_books()
        self.processor.add_personal_choice_books()
        df = self.processor.create_dataframe()
        
        results = self.processor.search_books('Computer', 'title')
        self.assertTrue(len(results) > 0)

if __name__ == '__main__':
    unittest.main()