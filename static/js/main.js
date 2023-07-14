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
        location.reload()
        // Reloads the movies in the delete endpoint after deleting one
    })
    .catch(error => console.error('Error:', error));  // If an error occurs, log it to the console
}


//// Function to show modal popup
//function openPopup(postId) {
//    var modal = document.getElementById('myModal');
//    modal.style.display = 'block';
//
//    // Sets the popup's form variables as empty and ID as the post ID
//    var formId = document.getElementById('id');
//    var formTitle = document.getElementById('title');
//    var formContent = document.getElementById('content');
//    var formAuthor = document.getElementById('author');
//    var formDate = document.getElementById('date');
//    formId.value = postId
//    formTitle.value = '';
//    formContent.value = '';
//    formAuthor.value = '';
//    formDate.value = '';
//
//    var form = document.getElementById('updateForm');
//    form.addEventListener('submit', function (event) {
//        event.preventDefault();
//
//        var id = formId.value;
//        var title = formTitle.value;
//        var content = formContent.value;
//        var author = formAuthor.value;
//        var date = formDate.value;
//
//        submitData(postId, title, content, author, date);
//        closePopup();
//    });
//}
//
//// Function to hide the modal popup
//function closePopup() {
//    var modal = document.getElementById('myModal');
//    modal.style.display = 'none';
//}
