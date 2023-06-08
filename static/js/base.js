// Toggle the navigation bar //
var topnavToggle = document.getElementById("topnavToggle-A");
topnavToggle.addEventListener("click", function(e) {
  var topnav = document.getElementById("topnav-A");
  if (topnav.className === "topnav") {
    topnav.classList.add("toggle");
  } else {
    topnav.className = "topnav";
  }
});
