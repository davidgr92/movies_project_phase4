from flask import Flask, render_template, request, redirect, url_for
from data_manager.dm_json import JSONDataManager
from moviweb_project.modules.omdb_api import MovieAPIRequest

app = Flask(__name__)
data_manager = JSONDataManager()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/users/')
@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return render_template('users.html', title='Users - MovieWeb App',
                           users=users)


@app.route('/users/<int:user_id>/')
@app.route('/users/<int:user_id>')
def get_user_movies(user_id):
    # TODO - Add error handling if user_id out of bound
    user = data_manager.get_user(user_id)
    return render_template('user_movies.html',
                           title=f"{user['name']}'s Favorite Movies",
                           user=user)


@app.route('/add_user/', methods=['GET', 'POST'])
@app.route('/add_user', methods=['GET', 'POST'])
def add_new_user():
    if request.method == 'GET':
        return render_template('add_user.html', title='Add New User',
                               heading='Add new user')
    elif request.method == 'POST':
        users = data_manager.get_all_users()
        new_id = max(user['id'] for user in users) + 1
        new_user = {"id": new_id,
                    "name": request.form.get('name'),
                    "movies": []}
        if new_user['name'] is None:
            return {'error': 'Bad Request - Empty name'}, 400
        data_manager.add_user(new_user)
        return redirect(url_for("add_new_user_movie", user_id=new_id)), 201


@app.route('/users/<int:user_id>/add_movie/', methods=['GET', 'POST'])
@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_new_user_movie(user_id):
    if request.method == 'GET':
        # TODO - Add error handling if user_id out of bound
        return render_template('add_user_movie.html',
                               title='Add New Favorite Movie',
                               user_id=user_id)
    elif request.method == 'POST':
        movies = data_manager.get_user_movies(user_id)
        connection = MovieAPIRequest()
        movie_name = request.form.get('movie-name')
        new_movie = connection.get_movie_data(movie_name)
        for movie in movies:
            if movie['name'].lower == new_movie['name'].lower():
                msg = 'Movie already exists, try again.'
                return redirect(url_for("add_new_user_movie",
                                        user_id=user_id, error_message=msg))
        if 'error' in new_movie:
            msg = new_movie['error']
            return redirect(url_for("add_new_user_movie",
                                    user_id=user_id, error_message=msg))
        else:
            if len(movies) < 1:
                new_movie_id = 1
            else:
                new_movie_id = max(movie["id"] for movie in movies) + 1
            new_movie.update({'id': new_movie_id})
            data_manager.add_user_movie(user_id, new_movie)
            return redirect(url_for('get_user_movies', user_id=user_id))


@app.route('/users/<int:user_id>/update_movie/<int:movie_id>/', methods=['GET', 'POST'])
@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_user_movie(user_id, movie_id):
    if request.method == 'GET':
        # TODO - Add error handling if user_id out of bound
        # TODO - Add error handling if movie_id out of bound
        movie = data_manager.get_user_single_movie(user_id, movie_id)
        return render_template('update_user_movie.html', user_id=user_id,
                               title=f'Updating Movie: {movie["name"]}',
                               movie=movie)
    elif request.method == 'POST':
        updated_movie = dict(request.form)
        data_manager.update_user_movie(user_id, movie_id, updated_movie)
        return redirect(url_for('get_user_movies', user_id=user_id))


@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>/', methods=['DELETE'])
@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>', methods=['DELETE'])
def delete_user_movie(user_id, movie_id):
    # TODO Create js delete function to call the DELETE method on this route
    # TODO update delete button in user's movies page to call del func
    data_manager.delete_user_movie(user_id, movie_id)
    return '', 200


@app.errorhandler(404)
def error_404(error):
    return render_template('404.html', title="Page not found 404")


if __name__ == '__main__':
    app.run(debug=True)


# TODO add error codes to API request responses (200/201/404...)
# TODO add button "Add movie" to user with empty movies list
# TODO add dynamic main nav to header

# TODO when adding a new movie - test that movie doesn't exist

# TODO test manually all pages and all functions edge-cases (try to prompt all available errors)
# TODO create unit tests to the flask application (based on previous manual checks)
# TODO test with pylint all styling

# TODO consider updating the way data is saved (use id's as keys in users + movies)
