import pytest
from os.path import isfile
from moviweb_project.data_manager.dm_json import JSONDataManager, DataManagerInterface

TEST_PATH = 'test.json'
MOVIE_TEST_DICT = {
    "id": 1,
    "name": "Inception",
    "director": "Christopher Nolan",
    "year": 2010,
    "rating": 8.8
}
USER_TEST_DICT = {
    "id": 1,
    "name": "Test",
    "movies": [MOVIE_TEST_DICT]
}
UPDATE_MOVIE_DICT = {
    "id": 1,
    "name": "Inception",
    "director": "Christopher Nolan",
    "year": 2010,
    "rating": 8.9,
    "note": "Personal note"
}
UPDATE_USER_DICT = {
    "id": 2,
    "name": "Tester",
    "movies": [UPDATE_MOVIE_DICT]
}
DELETE_USER_DICT = {
    "id": 2,
    "name": "Tester",
    "movies": []
}


# Before running test make sure the file 'test.json' is deleted
def test_init_non_existing_file():
    """Tests init and save to file"""
    storage = JSONDataManager(TEST_PATH)
    assert isinstance(storage, JSONDataManager)
    assert isinstance(storage, DataManagerInterface)
    assert isfile(TEST_PATH)


def test_get_all_users_add_user():
    """Tests get all users on empty file, add new user
    and get all users with non-empty file"""
    storage = JSONDataManager(TEST_PATH)
    storage.add_user(USER_TEST_DICT)
    assert storage.get_all_users() == [USER_TEST_DICT]


def test_get_user_movies_add_user_movie():
    """Tests get all user movies on empty movies list, add new movie
    and get all users movies with non-empty movies list"""
    storage = JSONDataManager(TEST_PATH)
    user_id = 1
    storage.add_user_movie(user_id, MOVIE_TEST_DICT)
    assert storage.get_user_movies(user_id) == [MOVIE_TEST_DICT]


def test_update_user_movie():
    """Test update user movie"""
    storage = JSONDataManager(TEST_PATH)
    user_id = movie_id = 1
    storage.update_user_movie(user_id, movie_id, UPDATE_MOVIE_DICT)
    assert storage.get_user_movies(user_id) == [UPDATE_MOVIE_DICT]


def test_update_user():
    """Test update user"""
    storage = JSONDataManager(TEST_PATH)
    user_id = 1
    storage.update_user(user_id, UPDATE_USER_DICT)
    assert storage.get_all_users() == [UPDATE_USER_DICT]


def test_delete_user_movie():
    """Test delete user movie"""
    storage = JSONDataManager(TEST_PATH)
    user_id = 2
    movie_id = 1
    assert storage.get_user_movies(user_id) == [UPDATE_MOVIE_DICT]
    storage.delete_user_movie(user_id, movie_id)
    assert storage.get_user_movies(user_id) == []


def test_delete_user():
    """Test delete user"""
    storage = JSONDataManager(TEST_PATH)
    user_id = 2
    assert storage.get_all_users() == [DELETE_USER_DICT]
    storage.delete_user(user_id)
    assert storage.get_all_users() == []


pytest.main()
