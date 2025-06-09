from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import config
from models.book import db, Book
from forms.book_forms import BookForm, SearchForm
import os
import pandas as pd
from ma_bib import LibraryDataProcessor

def create_app(config_name=None):
    '''Application factory pattern'''
    app = Flask(__name__)
    
    # Load configuration
    config_name = config_name or os.environ.get('FLASK_CONFIG', 'default')
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    
    def initialize_sample_data():
        '''Initialize database with sample data from ma_bib.py'''
        processor = LibraryDataProcessor()
        processor.add_sample_imsi_books()
        processor.add_personal_choice_books()
        
        for book_data in processor.books_data:
            book = Book(
                title=book_data['title'],
                author=book_data['author'],
                year=book_data['year'],
                isbn=book_data['isbn'],
                publisher=book_data['publisher'],
                genre=book_data['genre'],
                pages=book_data['pages'],
                language=book_data['language'],
                source=book_data['source'],
                description=book_data['description']
            )
            db.session.add(book)
        
        db.session.commit()
    
    # Create database tables
    with app.app_context():
        db.create_all()
        
        # Initialize with sample data if database is empty
        if Book.query.count() == 0:
            initialize_sample_data()
    
    # Routes
    @app.route('/')
    def index():
        '''Home page showing recent books and statistics'''
        recent_books = Book.query.order_by(Book.date_added.desc()).limit(5).all()
        total_books = Book.query.count()
        
        # Get statistics
        stats = {
            'total_books': total_books,
            'sources': db.session.query(Book.source, db.func.count(Book.id)).group_by(Book.source).all(),
            'genres': db.session.query(Book.genre, db.func.count(Book.id)).group_by(Book.genre).all()
        }
        
        return render_template('index.html', recent_books=recent_books, stats=stats)
    
    @app.route('/books')
    def books():
        '''Display all books with pagination'''
        page = request.args.get('page', 1, type=int)
        books = Book.query.order_by(Book.title).paginate(
            page=page, 
            per_page=app.config['BOOKS_PER_PAGE'],
            error_out=False
        )
        return render_template('books.html', books=books)
    
    @app.route('/book/<int:id>')
    def book_detail(id):
        '''Display detailed information about a specific book'''
        book = Book.query.get_or_404(id)
        return render_template('book_detail.html', book=book)
    
    @app.route('/add_book', methods=['GET', 'POST'])
    def add_book():
        '''Add a new book to the library'''
        form = BookForm()
        
        if form.validate_on_submit():
            book = Book(
                title=form.title.data,
                author=form.author.data,
                year=form.year.data,
                isbn=form.isbn.data,
                publisher=form.publisher.data,
                genre=form.genre.data,
                pages=form.pages.data,
                language=form.language.data,
                source=form.source.data,
                description=form.description.data,
                available=form.available.data
            )
            
            try:
                db.session.add(book)
                db.session.commit()
                flash('Book added successfully!', 'success')
                return redirect(url_for('book_detail', id=book.id))
            except Exception as e:
                db.session.rollback()
                flash('Error adding book. Please try again.', 'error')
        
        return render_template('add_book.html', form=form)
    
    @app.route('/search', methods=['GET', 'POST'])
    def search():
        '''Search books functionality'''
        form = SearchForm()
        results = []
        
        if form.validate_on_submit():
            query = form.query.data
            field = form.field.data
            
            results = Book.search(query, field if field != 'all' else None)
            
            if not results:
                flash(f'No books found for "{query}"', 'info')
        
        return render_template('search.html', form=form, results=results)
    
    @app.route('/api/books')
    def api_books():
        '''API endpoint to get books as JSON'''
        books = Book.query.all()
        return jsonify([book.to_dict() for book in books])
    
    @app.route('/api/search')
    def api_search():
        '''API endpoint for search functionality'''
        query = request.args.get('q', '')
        field = request.args.get('field', 'all')
        
        if not query:
            return jsonify({'error': 'Query parameter required'}), 400
        
        results = Book.search(query, field if field != 'all' else None)
        return jsonify([book.to_dict() for book in results])
    
    @app.route('/export/csv')
    def export_csv():
        '''Export library data to CSV'''
        books = Book.query.all()
        data = [book.to_dict() for book in books]
        df = pd.DataFrame(data)
        
        # Save to temporary file
        filename = 'mektabati_export.csv'
        df.to_csv(filename, index=False)
        
        flash(f'Data exported to {filename}', 'success')
        return redirect(url_for('index'))
    
    @app.route('/dataframe')
    def dataframe_view():
        '''Display DataFrame analysis from ma_bib.py'''
        processor = LibraryDataProcessor()
        processor.add_sample_imsi_books()
        processor.add_personal_choice_books()
        df = processor.create_dataframe()
        stats = processor.get_statistics()
        
        # Convert DataFrame to HTML
        df_html = df.to_html(classes='table table-striped', table_id='dataframe-table')
        
        return render_template('dataframe.html', df_html=df_html, stats=stats)
    
    return app

# Create the application
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)