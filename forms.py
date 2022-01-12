from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, TextAreaField
from wtforms.validators import DataRequired


class Movie_Title(FlaskForm):
    movie_title = StringField(label="Movie Title", validators=[DataRequired()])
    submit = SubmitField(label="Submit")


class Movie_Rating(FlaskForm):
    movie_rating = FloatField(label="Your Rating out of 10 (eg. 7.5)")
    movie_review = TextAreaField("Your Movie Review",
                                 render_kw={
                                     "rows": 5,
                                     "cols": 11
                                 })
    submit = SubmitField(label="Submit")
