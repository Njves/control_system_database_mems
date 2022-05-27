const image = document.getElementById('meme_image')
function fail() {
    image.src = "https://klike.net/uploads/posts/2019-04/1555138528_1.jpg"
}
image.addEventListener('error', fail);

// The DOM element you wish to replace with Tagify
var input = document.querySelector('input[name=tags]');

// initialize Tagify on the above input node reference
new Tagify(input)

