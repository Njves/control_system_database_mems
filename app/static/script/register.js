const requestUrl = 'http://127.0.0.1:5000/registration';

const xhr = new XMLHttpRequest();




// Событие нажатия кнопки
document.getElementById('register_button').addEventListener('click', function(event){
    xhr.open('POST', requestUrl);
    let username = document.getElementById('basic-username').value;
    let email = document.getElementById('basic-username').value;
    let password = document.getElementById('basic-password').value;
    let data = new FormData();
    data.append('username', username)
    data.append('email', email)
    data.append('password', password)
    xhr.send(data);



});
// callback при выполнение запроса
xhr.onload = function() {
    console.log(this.responseText)
}

