const avatar = document.getElementById('avatar')
function fail() {
    avatar.src = "http://127.0.0.1:5000/static/images/avatars/avatar_placeholder.png"
}
avatar.addEventListener('error', fail);
const containerTags = document.getElementById('containerTags');


function allowDrop(event) {
    event.preventDefault();
}
const handleImageUpload = event => {
  const files = event.target.files
  const formData = new FormData()
  formData.append('image', files[0])
  formData.append('name', "random")
  formData.append('tags', "random1")
  fetch('/upload', {
    method: 'POST',
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    console.log(data.path)
  })
  .catch(error => {
    console.error(error)
  })
}
memFile.onchange = function(event){
    handleImageUpload(event)
}



