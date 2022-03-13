const requestUrl = 'http://127.0.0.1:5000/register';

const xhr = new XMLHttpRequest();

document.getElementById('register_button').addEventListener('click', function(event){
    xhr.open('GET', requestUrl);
    xhr.send();
});
xhr.onload = function() {
        console.log(xhr.response)
}

