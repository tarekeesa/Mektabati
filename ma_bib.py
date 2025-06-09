#!/usr/bin/env python3
'''
ma_bib.py - Core library data processing module
This module handles data collection, processing, and DataFrame operations
as required for the Mektabati assignment.
'''

import pandas as pd
from datetime import datetime
import json

class LibraryDataProcessor:
    '''
    Core class for processing library data and creating DataFrames
    '''
    
    def __init__(self):
        self.books_data = []
        self.df = None
    
    def add_sample_imsi_books(self):
        '''Add 1.5 books from IMSI library as required'''
        imsi_books = [
            {
                'title': 'Introduction to Computer Science',
                'author': 'Ahmed Ben Ali',
                'year': 2020,
                'isbn': '978-123456789',
                'publisher': 'IMSI Press',
                'genre': 'Technology',
                'pages': 350,
                'language': 'French',
                'source': 'IMSI Library',
                'description': 'Comprehensive introduction to computer science concepts'
            },
            # This represents the "0.5" book - a partial/reference book
            {
                'title': 'Mathematics for Engineers (Reference)',
                'author': 'Dr. Sarah Mohamed',
                'year': 2019,
                'isbn': '978-987654321',
                'publisher': 'IMSI Press',
                'genre': 'Science',
                'pages': 200,
                'language': 'French',
                'source': 'IMSI Library',
                'description': 'Mathematical concepts reference for engineering students'
            }
        ]
        self.books_data.extend(imsi_books)
    
    def add_personal_choice_books(self):
        '''Add 5 books of personal choice from various sources'''
        personal_books = [
            {
                'title': 'Les Misérables',
                'author': 'Victor Hugo',
                'year': 1862,
                'isbn': '978-111111111',
                'publisher': 'Lacroix, Verboeckhoven & Cie',
                'genre': 'Literature',
                'pages': 1232,
                'language': 'French',
                'source': 'Municipal Library',
                'description': 'Classic French novel about social justice and redemption'
            },
            {
                'title': 'The Alchemist',
                'author': 'Paulo Coelho',
                'year': 1988,
                'isbn': '978-222222222',
                'publisher': 'HarperCollins',
                'genre': 'Fiction',
                'pages': 163,
                'language': 'English',
                'source': 'Personal Collection',
                'description': 'Philosophical novel about following your dreams'
            },
            {
                'title': 'A Brief History of Time',
                'author': 'Stephen Hawking',
                'year': 1988,
                'isbn': '978-333333333',
                'publisher': 'Bantam Books',
                'genre': 'Science',
                'pages': 256,
                'language': 'English',
                'source': 'University Library',
                'description': 'Popular science book about cosmology and black holes'
            },
            {
                'title': 'The Bible',
                'author': 'Various',
                'year': None,
                'isbn': '978-444444444',
                'publisher': 'Oxford University Press',
                'genre': 'Religion',
                'pages': 1200,
                'language': 'French',
                'source': 'Cathedral Library',
                'description': 'Holy book of Christianity'
            },
            {
                'title': 'Clean Code',
                'author': 'Robert C. Martin',
                'year': 2008,
                'isbn': '978-555555555',
                'publisher': 'Prentice Hall',
                'genre': 'Technology',
                'pages': 464,
                'language': 'English',
                'source': 'Personal Collection',
                'description': 'Guide to writing clean, maintainable code'
            }
        ]
        self.books_data.extend(personal_books)
    
    def create_dataframe(self):
        '''Create pandas DataFrame from collected book data'''
        self.df = pd.DataFrame(self.books_data)
        return self.df
    
    def search_books(self, query, field='all'):
        '''
        Search functionality for the DataFrame
        Args:
            query: Search term
            field: Field to search in ('title', 'author', 'year', 'genre', 'all')
        '''
        if self.df is None:
            return pd.DataFrame()
        
        if field == 'all':
            # Search across multiple text fields
            mask = (
                self.df['title'].str.contains(query, case=False, na=False) |
                self.df['author'].str.contains(query, case=False, na=False) |
                self.df['genre'].str.contains(query, case=False, na=False) |
                self.df['publisher'].str.contains(query, case=False, na=False)
            )
        elif field == 'year':
            try:
                year = int(query)
                mask = self.df['year'] == year
            except ValueError:
                return pd.DataFrame()
        else:
            mask = self.df[field].str.contains(query, case=False, na=False)
        
        return self.df[mask]
    
    def get_statistics(self):
        '''Get library statistics'''
        if self.df is None:
            return {}
        
        stats = {
            'total_books': len(self.df),
            'books_by_source': self.df['source'].value_counts().to_dict(),
            'books_by_genre': self.df['genre'].value_counts().to_dict(),
            'books_by_language': self.df['language'].value_counts().to_dict(),
            'average_pages': self.df['pages'].mean() if 'pages' in self.df else 0,
            'year_range': {
                'earliest': int(self.df['year'].min()) if self.df['year'].notna().any() else None,
                'latest': int(self.df['year'].max()) if self.df['year'].notna().any() else None
            }
        }
        return stats
    
    def export_to_csv(self, filename='library_data.csv'):
        '''Export DataFrame to CSV file'''
        if self.df is not None:
            self.df.to_csv(filename, index=False)
            return f"Data exported to {filename}"
        return "No data to export"
    
    def export_to_json(self, filename='library_data.json'):
        '''Export data to JSON file'''
        if self.books_data:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.books_data, f, indent=2, ensure_ascii=False)
            return f"Data exported to {filename}"
        return "No data to export"

def main():
    '''Main function to demonstrate the library data processing'''
    print("Mektabati - Library Data Processing")
    print("=" * 40)
    
    # Initialize processor
    processor = LibraryDataProcessor()
    
    # Add books as required by assignment
    print("Adding IMSI library books...")
    processor.add_sample_imsi_books()
    
    print("Adding personal choice books...")
    processor.add_personal_choice_books()
    
    # Create DataFrame
    print("Creating DataFrame...")
    df = processor.create_dataframe()
    
    # Display data
    print(f"\\nLibrary DataFrame (Shape: {df.shape}):")
    print(df.to_string())
    
    # Demonstrate search functionality
    print("\\nSearch Examples:")
    print("-" * 20)
    
    # Search by title
    search_result = processor.search_books("Computer", "title")
    print(f"Books with 'Computer' in title: {len(search_result)}")
    
    # Search by author
    search_result = processor.search_books("Hugo", "author")
    print(f"Books by authors containing 'Hugo': {len(search_result)}")
    
    # Search by year
    search_result = processor.search_books("2020", "year")
    print(f"Books from 2020: {len(search_result)}")
    
    # Get statistics
    stats = processor.get_statistics()
    print("\\nLibrary Statistics:")
    print("-" * 20)
    print(f"Total books: {stats['total_books']}")
    print(f"Books by source: {stats['books_by_source']}")
    print(f"Books by genre: {stats['books_by_genre']}")
    
    # Export data
    print("\\nExporting data...")
    processor.export_to_csv()
    processor.export_to_json()
    print("Data exported successfully!")

if __name__ == "__main__":
    main()