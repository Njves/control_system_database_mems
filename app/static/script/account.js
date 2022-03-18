const avatar = document.getElementById('avatar')
function fail() {
    avatar.src = "http://127.0.0.1:5000/static/images/avatars/avatar_placeholder.png"
}
avatar.addEventListener('error', fail);
const containerTags = document.getElementById('containerTags');
containerTags.ondragover = allowDrop;

function allowDrop(event) {
    event.preventDefault();
}

