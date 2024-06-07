

var canvas = document.getElementById("canvas");
document.getElementById("container").style.display="none";
var context = canvas.getContext("2d");
const video = document.querySelector("#videoElement");



if (navigator.mediaDevices.getUserMedia) {
  navigator.mediaDevices
    .getUserMedia({
      video: true,
    })
    .then(function (stream) {
      video.srcObject = stream;
      video.play();
    })
    .catch(function (err0r) {});
}
const FPS = 12;
setInterval(() => {
  width = canvas.width;
  height = canvas.height;
  context.drawImage(video, 0, 0, width, height);
  var data = canvas.toDataURL("image/jpeg", 0.5);
  context.clearRect(0, 0, width, height);
  socket.emit("image", data);
  console.log(1)
}, 1000 / FPS);

socket.on("processed_image", function (image) {

  photo.setAttribute("src", image);
});