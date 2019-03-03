window.onload = function () {
    email_button = document.getElementById("email-button");
    email_button.onclick = function(){
        email_input = document.getElementById("email-input");
        if (email_input.checkValidity()) {
            var http = new XMLHttpRequest();
            http.onreadystatechange = function() {
                if (http.readyState == XMLHttpRequest.DONE) {
                    response = JSON.parse(http.responseText);
                    if (response.state != 'ok') {
                        alert(response.msg);
                    } else {
                        email_input.value = '';
                        alert(response.msg);
                    }
                }
            }
            http.open('POST', 'api/register-email', true);
            http.setRequestHeader("Content-Type", "application/json");
            result = http.send(JSON.stringify({'email': email_input.value}));
            }
        else {
            alert("email not valid")
        }
    };
}