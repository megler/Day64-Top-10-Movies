# Top 10 Movies App

A Flask app that lists your top 10 Movies. Day 31 Python Bootcamp

## Usage

This app uses Flask, SQLAlchemy and the [The Movie Database API](https://www.themoviedb.org/documentation/api)
to list your top 10 movies.

The app allows you to do CRUD funcitons by adding a movie, reading saved movies
from the database, updating rating and description and deleting movies.

When you add a movie title, the app queries the TMDB api and lists all movies
matching your keyword (eg. "Batman"). When you click the link of the movie you
want, it will be added to the database and the app homepage is now updated with
your entry.

You can now edit/add a rating and description. Once a rating is saved, the app
will sort the movies in descending order (10 -> 1). If you change a rating, the
app will re-sort based on the new standings.

## License

[MIT](https://choosealicense.com/licenses/mit/)
