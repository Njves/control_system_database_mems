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
  .then(response => {
    response.json()
    location.reload()
  })
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

// Реализация Drag&Drop

const types = ['image/jpeg', 'image/png']

let dragAndDrop = document.querySelector('.dragAndDrop')
let placeDragAndDrop = document.querySelector('.placeDragAndDrop')
let checkDragAndDrop = false
let checkPlaceDragAndDrop = true
let checkLeave = false
let count = 0

function enter(event) {
  event.preventDefault()
  placeDragAndDrop.style.visibility = 'visible'
}

function enterPlaceDragAndDrop(event) {
  event.preventDefault()
  if(checkDragAndDrop) count += 1
  if(count == 2) {
    checkLeave = false
    checkPlaceDragAndDrop = false
  }
}

function leavePlaceDragAndDrop(event) {
  event.preventDefault()
  if(checkPlaceDragAndDrop && (count != 1)) {
    placeDragAndDrop.style.visibility = 'hidden'
    addEventListener('dragenter', enter, {once : true})
    dragAndDrop.innerHTML = 'Перетащите сюда мем'
  }
  checkPlaceDragAndDrop = true
}

placeDragAndDrop.addEventListener('dragenter', enterPlaceDragAndDrop)

placeDragAndDrop.addEventListener('dragleave', leavePlaceDragAndDrop)

placeDragAndDrop.addEventListener('dragover', event => {
  event.preventDefault()
})


//Здесь происходит загрузка картинок (событие выполняется один раз если за облостью квадратика розового,
// Если внутри розового квадратика, то событие выполняется два раза
// Поэтому если будут какие-то проблемы с загрузкой картинки, пиши мне, я уберу это
placeDragAndDrop.addEventListener('drop', event => {
  event.preventDefault()
  let file = event.dataTransfer.files
  if(!((file.length == 1) && types.includes(file[0].type))) {
    console.log("Error file")
    // Делаю файл пустым, если скинули больше одного файла или не тот тип
    // Дизайн и анимации потом сделаю
    file = null
  }
})



dragAndDrop.addEventListener('dragenter', event => {
  event.preventDefault()
  checkDragAndDrop = true
  checkLeave = true
})

dragAndDrop.addEventListener('dragleave', event => {
  event.preventDefault()
  checkDragAndDrop = false
  count = 0
  if(checkLeave) {
    checkLeave = false
  }
})

dragAndDrop.addEventListener('dragover', event => {
  event.preventDefault()
})

dragAndDrop.addEventListener('drop', event => {
  event.preventDefault()
})

addEventListener('dragenter', enter, {once : true})