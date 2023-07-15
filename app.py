from flask import Flask, render_template, request, redirect, url_for, abort
from data_manager.dm_json import JSONDataManager
from moviweb_project.modules.omdb_api import MovieAPIConnection

app = Flask(__name__)
data_manager = JSONDataManager()


def get_new_id(data):
    """Returns new id based on data"""
    if len(data) < 1:
        return 1
    return max(item["id"] for item in data) + 1


@app.route('/users')
@app.route('/')
def list_users():
    """Returns main page - lists all users"""
    users = data_manager.get_all_users()
    return render_template('users.html', title='Users',
                           users=users)


@app.route('/users/<int:user_id>')
def get_user_movies(user_id):
    """Returns specific user movies list, handles wrong id error"""
    user = data_manager.get_user(user_id)
    if not data_manager.is_user_id_exists(user_id):
        abort(404, "Failed to find user with this ID.")
    return render_template('user_movies.html',
                           title=f"{user['name']}'s Movies",
                           user=user)


@app.route('/users/<int:user_id>/delete/', methods=['DELETE'])
def delete_user(user_id):
    """Deletes user from data file, handles wrong id error"""
    data_manager.delete_user(user_id)
    if not data_manager.is_user_id_exists(user_id):
        abort(404, "Failed to find user with this ID.")
    return ''


@app.route('/add_user', methods=['GET', 'POST'])
def add_new_user():
    """When used with GET method, returns form page to register a new user,
    When used with POST method, validates data and sign up the user.
    Shows errors and success message accordingly."""
    if request.method == 'GET':
        return render_template('add_user.html', title='Add New User',
                               heading='Add new user')
    # In case of a POST request method
    users = data_manager.get_all_users()
    new_user = {"id": get_new_id(users),
                "name": request.form.get('name'),
                "movies": []}
    if new_user['name'] == '':
        error = "Invalid new user request - provided empty name"
        return render_template('add_user.html', title='Add New User',
                               heading='Add new user',
                               error_message=error)
    data_manager.add_user(new_user)
    success = "User was successfully created! Now you can add a movie."
    return render_template('add_user_movie.html',
                           title='Add New Favorite Movie',
                           user_id=new_user['id'],
                           success_message=success)


@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_new_user_movie(user_id):
    """When used with GET method, returns form page to add new movie,
    When used with POST method sends request to omdb movies api to get
    movie details, and adds to data file. Handles errors with user id,
    movie api and data manager"""
    if request.method == 'GET':
        if not data_manager.is_user_id_exists(user_id):
            abort(404, "Failed to find user with this ID.")
        return render_template('add_user_movie.html',
                               title='Add New Favorite Movie',
                               user_id=user_id)

    # In case of a POST request method
    movies = data_manager.get_user_movies(user_id)
    connection = MovieAPIConnection()
    new_movie = connection.get_movie_data(request.form.get('movie-name'))

    # Handle errors in the response from the MovieAPI
    if 'error' in new_movie:
        error = new_movie['error']
        return render_template('add_user_movie.html',
                               title='Add New Favorite Movie',
                               user_id=user_id,
                               error_message=error)

    new_movie_id = get_new_id(movies)
    new_movie.update({'id': new_movie_id})

    # Handle errors from the data manager
    try:
        data_manager.add_user_movie(user_id, new_movie)
    except ValueError as error:
        return render_template('add_user_movie.html',
                               title='Add New Favorite Movie',
                               user_id=user_id,
                               error_message=error)

    return redirect(url_for('get_user_movies', user_id=user_id))


@app.route('/users/<int:user_id>/update_movie/<int:movie_id>',
           methods=['GET', 'POST'])
def update_user_movie(user_id, movie_id):
    """When used with GET method, returns form page to update the movie,
    When used with POST method updates the movie details on file.
    Handles wrong id error"""
    if request.method == 'GET':
        if not data_manager.is_user_id_exists(user_id):
            abort(404, "Failed to find user with this ID.")
        if not data_manager.is_movie_id_exists(user_id, movie_id):
            abort(404, "Failed to find movie with this ID.")
        movie = data_manager.get_user_single_movie(user_id, movie_id)
        return render_template('update_user_movie.html', user_id=user_id,
                               title=f'Updating Movie: {movie["name"]}',
                               movie=movie)

    # In case of a POST request method
    updated_movie = dict(request.form)
    data_manager.update_user_movie(user_id, movie_id, updated_movie)
    return redirect(url_for('get_user_movies', user_id=user_id))


@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>',
           methods=['DELETE'])
def delete_user_movie(user_id, movie_id):
    """Deletes a movie from user's movie list in data file"""
    data_manager.delete_user_movie(user_id, movie_id)
    return ''


@app.errorhandler(404)
def error_404(error):
    """Renders 404.html page when user reaches a Page Not Found error page"""
    return render_template('404.html', title="Page not found 404",
                           error_message=error)


@app.errorhandler(400)
def error_400(error):
    """Renders 400.html page when user reaches a Bad Request error page"""
    return render_template('400.html', title="Bad request 400",
                           error_message=error)


if __name__ == '__main__':
    app.run(debug=True)
