from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def hello_world():
    return "Hello world"

# Home (/): This will be the home page of our application. You have the creative liberty to design this as a simple welcome screen or a more elaborate dashboard.

# Users List (/users): This route will present a list of all users registered in our MovieWeb App.

# User Movies (/users/<user_id>): This route will exhibit a specific user’s list of favorite movies. We will use the <user_id> in the route to fetch the appropriate user’s movies.

# Add User (/add_user): This route will present a form that enables the addition of a new user to our MovieWeb App.

# Add Movie (/users/<user_id>/add_movie): This route will display a form to add a new movie to a user’s list of favorite movies.

# Update Movie (/users/<user_id>/update_movie/<movie_id>): This route will display a form allowing for the updating of details of a specific movie in a user’s list.

# Edit Movie (/users/<user_id>/edit_movie/<movie_id>): This route will show a form allowing the modification of a specific movie in a user’s favorite movie list.

# Delete Movie (/users/<user_id>/delete_movie/<movie_id>): Upon visiting this route, a specific movie will be removed from a user’s favorite movie list.

if __name__ == '__main__':
    app.run(debug=True)