alert('dsf');
function login(){
    $.ajax({
        contentType: "application/json",
        url: 'http://localhost:5000/login',
        type: 'POST',
        
        data: JSON.Parse({
            
            username: $('username').txt,
            password: $('password').txt
        }),
        success: function(response) {
        alert('success')
        },
        error: function(xhr, status, error) {
            console.error(error);
        }
    });
}
