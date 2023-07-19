
function fail() {
    console.log("fail")
    avatar.src = "http://127.0.0.1:5000/static/images/avatars/avatar_placeholder.png"
}
avatar.addEventListener('error', fail);
const containerTags = document.getElementById('containerTags');

function allowDrop(event) {
  event.preventDefault();
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
  if (checkDragAndDrop) count += 1
  if (count == 2) {
    checkLeave = false
    checkPlaceDragAndDrop = false
  }
}

function leavePlaceDragAndDrop(event) {
  event.preventDefault()
  if (checkPlaceDragAndDrop && (count != 1)) {
    placeDragAndDrop.style.visibility = 'hidden'
    addEventListener('dragenter', enter, { once: true })
    dragAndDrop.innerHTML = 'Перетащите сюда мем'
  }
  checkPlaceDragAndDrop = true
}

placeDragAndDrop.addEventListener('dragenter', enterPlaceDragAndDrop)

placeDragAndDrop.addEventListener('dragleave', leavePlaceDragAndDrop)

placeDragAndDrop.addEventListener('dragover', event => {
  event.preventDefault()
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
  if (checkLeave) {
    checkLeave = false
  }
})

dragAndDrop.addEventListener('dragover', event => {
  event.preventDefault()
})

dragAndDrop.addEventListener('drop', event => {
  event.preventDefault()
})

addEventListener('dragenter', enter, { once: true })
