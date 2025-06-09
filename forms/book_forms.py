from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Optional, Length, NumberRange
from models.book import Book

class BookForm(FlaskForm):
    '''Form for adding/editing books'''
    
    title = StringField('Title', validators=[
        DataRequired(message='Title is required'),
        Length(max=200, message='Title must be less than 200 characters')
    ])
    
    author = StringField('Author', validators=[
        DataRequired(message='Author is required'),
        Length(max=100, message='Author name must be less than 100 characters')
    ])
    
    year = IntegerField('Publication Year', validators=[
        Optional(),
        NumberRange(min=1, max=2024, message='Year must be between 1 and 2024')
    ])
    
    isbn = StringField('ISBN', validators=[
        Optional(),
        Length(max=20, message='ISBN must be less than 20 characters')
    ])
    
    publisher = StringField('Publisher', validators=[
        Optional(),
        Length(max=100, message='Publisher name must be less than 100 characters')
    ])
    
    genre = SelectField('Genre', choices=[
        ('', 'Select Genre'),
        ('Fiction', 'Fiction'),
        ('Non-Fiction', 'Non-Fiction'),
        ('Science', 'Science'),
        ('History', 'History'),
        ('Biography', 'Biography'),
        ('Technology', 'Technology'),
        ('Literature', 'Literature'),
        ('Philosophy', 'Philosophy'),
        ('Religion', 'Religion'),
        ('Art', 'Art'),
        ('Other', 'Other')
    ], validators=[Optional()])
    
    pages = IntegerField('Number of Pages', validators=[
        Optional(),
        NumberRange(min=1, message='Pages must be a positive number')
    ])
    
    language = SelectField('Language', choices=[
        ('French', 'French'),
        ('English', 'English'),
        ('Arabic', 'Arabic'),
        ('Spanish', 'Spanish'),
        ('German', 'German'),
        ('Other', 'Other')
    ], default='French')
    
    source = SelectField('Source', choices=[
        ('IMSI Library', 'IMSI Library'),
        ('Personal Collection', 'Personal Collection'),
        ('Municipal Library', 'Municipal Library'),
        ('Cathedral Library', 'Cathedral Library'),
        ('University Library', 'University Library'),
        ('Online', 'Online'),
        ('Other', 'Other')
    ], validators=[DataRequired(message='Source is required')])
    
    description = TextAreaField('Description', validators=[
        Optional(),
        Length(max=1000, message='Description must be less than 1000 characters')
    ])
    
    available = BooleanField('Available', default=True)

class SearchForm(FlaskForm):
    '''Form for searching books'''
    
    query = StringField('Search', validators=[
        DataRequired(message='Please enter a search term')
    ])
    
    field = SelectField('Search In', choices=[
        ('all', 'All Fields'),
        ('title', 'Title'),
        ('author', 'Author'),
        ('year', 'Year'),
        ('genre', 'Genre')
    ], default='all')