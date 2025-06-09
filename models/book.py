from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Book(db.Model):
    '''
    Book model representing a book in the library
    '''
    __tablename__ = 'books'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    author = db.Column(db.String(100), nullable=False, index=True)
    year = db.Column(db.Integer, index=True)
    isbn = db.Column(db.String(20), unique=True)
    publisher = db.Column(db.String(100))
    genre = db.Column(db.String(50), index=True)
    pages = db.Column(db.Integer)
    language = db.Column(db.String(30), default='French')
    source = db.Column(db.String(100))  # IMSI library, personal, municipal, etc.
    description = db.Column(db.Text)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    available = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<Book {self.title} by {self.author}>'
    
    def to_dict(self):
        '''Convert book object to dictionary for JSON serialization'''
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'year': self.year,
            'isbn': self.isbn,
            'publisher': self.publisher,
            'genre': self.genre,
            'pages': self.pages,
            'language': self.language,
            'source': self.source,
            'description': self.description,
            'date_added': self.date_added.isoformat() if self.date_added else None,
            'available': self.available
        }
    
    @classmethod
    def search(cls, query, field=None):
        '''
        Search books by various fields
        Args:
            query: Search term
            field: Specific field to search in (title, author, genre, etc.)
        '''
        if field == 'title':
            return cls.query.filter(cls.title.contains(query)).all()
        elif field == 'author':
            return cls.query.filter(cls.author.contains(query)).all()
        elif field == 'year':
            try:
                year = int(query)
                return cls.query.filter(cls.year == year).all()
            except ValueError:
                return []
        elif field == 'genre':
            return cls.query.filter(cls.genre.contains(query)).all()
        else:
            # Search across multiple fields
            return cls.query.filter(
                db.or_(
                    cls.title.contains(query),
                    cls.author.contains(query),
                    cls.genre.contains(query),
                    cls.publisher.contains(query)
                )
            ).all()

class Author(db.Model):
    '''
    Author model for detailed author information
    '''
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    birth_year = db.Column(db.Integer)
    nationality = db.Column(db.String(50))
    biography = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Author {self.name}>'