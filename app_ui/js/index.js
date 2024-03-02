API_URL = "http://localhost:5000/"

function login(){
    $.ajax({
        contentType: "application/json",
        url: API_URL + encodeURIComponent('login'),
        type: 'POST',
        data: JSON.stringify({
            username: $('#username').val(),
            password: $('#password').val()
        }),
        success: function(response) {
            console.log(response)
            window.location.replace('home.html');
        },
        error: function(xhr, status, error) {
            result = xhr.responseJSON['message']
            console.error(status, error);
            alert(result);
        }
    });
}
