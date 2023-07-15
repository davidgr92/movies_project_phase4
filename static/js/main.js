// Function to send a DELETE request to the API to Delete a movie of specific user
function deleteUserMovie(userId, movieId) {
    var baseUrl = 'http://127.0.0.1:5000/'

    // Use the Fetch API to send a DELETE request to the specific post's endpoint
    var delete_endpoint = '/users/' + userId + '/delete_movie/' + movieId
    fetch(baseUrl + delete_endpoint, {
        method: 'DELETE'
    })
    .then(response => {
        console.log('Movie deleted:', movieId);
        location.reload()  // Reloads the movies in the delete endpoint after deleting one
    })
    .catch(error => console.error('Error:', error));  // If an error occurs, log it to the console
}

// Function to send a DELETE request to the API to Delete a specific user
function deleteUser(userId) {
    var baseUrl = 'http://127.0.0.1:5000/'

    // Use the Fetch API to send a DELETE request to the specific post's endpoint
    var delete_endpoint = '/users/' + userId + '/delete'
    fetch(baseUrl + delete_endpoint, {
        method: 'DELETE'
    })
    .then(response => {
        console.log('User deleted:', userId);
        location.reload()  // Reloads the movies in the delete endpoint after deleting one
    })
    .catch(error => console.error('Error:', error));  // If an error occurs, log it to the console
}
