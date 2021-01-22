from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired


class BooksForm(FlaskForm):
    Title = StringField(label='Tytuł', validators=[DataRequired()])
    Author = StringField(label='Autor', validators=[DataRequired()])
    Year = StringField(label='Rok powstania')
    Genre = StringField(label='Gatunek')
    Done = SelectField(label='Czy przeczytane?', choices=['Tak', 'Nie'])
