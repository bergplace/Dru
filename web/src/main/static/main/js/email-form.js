window.onload = function () {
    console.log("initializing js for email form");
    email_button = document.getElementById("email-button");
    email_button.onclick = function(){
        email_input = document.getElementById("email-input");
        var http = new XMLHttpRequest();
        http.onreadystatechange = function() {
            if (http.readyState == XMLHttpRequest.DONE) {
                response = JSON.parse(http.responseText);
                if (response.state != 'ok') {
                    alert(response.msg);
                } else {
                    email_input.value = '';
                    alert("email with link to verify have been sent");
                }
            }
        }
        http.open('POST', 'api/register-email', true);
        http.setRequestHeader("Content-Type", "application/json");
        result = http.send(JSON.stringify({'email': email_input.value}));
        console.log(result);
    };
    console.log("email register button scripted");
}