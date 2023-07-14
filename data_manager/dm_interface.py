from abc import ABC, abstractmethod


class DataManagerInterface(ABC):

    @abstractmethod
    def save_to_file(self, file_data):
        """Saves the provided data to file"""
        pass

    @abstractmethod
    def get_all_users(self):
        """Returns a list of all users from data file,
        each user data as a dict object."""
        pass

    @abstractmethod
    def add_user(self, user_dict):
        """Adds a new user to data file"""
        pass

    @abstractmethod
    def delete_user(self, user_id):
        """Deletes a user from data file"""
        pass

    @abstractmethod
    def update_user(self, user_id, update_dict):
        """Update user data in data file"""
        pass

    @abstractmethod
    def get_user(self, user_id):
        """Returns a user dict based on user_id"""
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        """Returns a list of user movies based on input user_id,
        each movie data as a dict object."""
        pass

    @abstractmethod
    def add_user_movie(self, user_id, movie_dict):
        """Adds a new movie to specific user in data file"""
        pass

    @abstractmethod
    def delete_user_movie(self, user_id, movie_id):
        """Deletes a movie from specific user in data file"""
        pass

    @abstractmethod
    def update_user_movie(self, user_id, movie_id, update_dict):
        """Update a movie from specific user in data file"""
        pass
