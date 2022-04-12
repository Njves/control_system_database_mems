const image = document.getElementById('meme_image')
function fail() {
    image.src = "https://klike.net/uploads/posts/2019-04/1555138528_1.jpg"
}
image.addEventListener('error', fail);

