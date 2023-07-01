import json
from os.path import isfile
from .dm_interface import DataManagerInterface


class JSONDataManager(DataManagerInterface):
    """Data manager class which interfaces with the JSON data file"""
    def __init__(self, filename="data.json"):
        self.filename = filename
        if not isfile(filename):
            self.save_to_file([])

    def save_to_file(self, data) -> None:
        """Saves the provided data to the json data file"""
        with open(self.filename, 'w') as file:
            file.write(json.dumps(data, indent=4))

    def get_all_users(self) -> list:
        """Returns a list of all users from data file,
        each user data as a dict object."""
        with open(self.filename, 'r') as file:
            return json.loads(file.read())

    def add_user(self, user_dict) -> None:
        """Adds a new user to data file"""
        users_list = self.get_all_users()
        user_ids = (user['id'] for user in users_list)
        if user_dict['id'] not in user_ids:
            users_list.append(user_dict)
            self.save_to_file(users_list)

    def delete_user(self, user_id) -> None:
        """Deletes a user from data file"""
        users_list = self.get_all_users()
        for user in users_list:
            if user['id'] == user_id:
                users_list.remove(user)
        self.save_to_file(users_list)

    def update_user(self, user_id, update_dict) -> None:
        """Update user data in data file"""
        users_list = self.get_all_users()
        for user in users_list:
            if user['id'] == user_id:
                user.update(update_dict)
        self.save_to_file(users_list)

    def get_user_movies(self, user_id) -> list:
        """Returns a list of user movies based on input user_id,
        each movie data as a dict object."""
        users_list = self.get_all_users()
        for user in users_list:
            if user['id'] == user_id:
                return user['movies']

    def add_user_movie(self, user_id, movie_dict) -> None:
        """Adds a new movie to specific user in data file"""
        users_list = self.get_all_users()
        for user in users_list:
            if user['id'] == user_id:
                movie_ids = (movie['id'] for movie in user['movies'])
                if movie_dict['id'] not in movie_ids:
                    user['movies'].append(movie_dict)
        self.save_to_file(users_list)

    def delete_user_movie(self, user_id, movie_id) -> None:
        """Deletes a movie from specific user in data file"""
        users_list = self.get_all_users()
        for user in users_list:
            if user['id'] == user_id:
                for movie in user['movies']:
                    if movie['id'] == movie_id:
                        user['movies'].remove(movie)
        self.save_to_file(users_list)

    def update_user_movie(self, user_id, movie_id, update_dict) -> None:
        """Update a movie from specific user in data file"""
        users_list = self.get_all_users()
        for user in users_list:
            if user['id'] == user_id:
                for movie in user['movies']:
                    if movie['id'] == movie_id:
                        movie.update(update_dict)
        self.save_to_file(users_list)
