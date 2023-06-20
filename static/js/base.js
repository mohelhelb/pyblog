import {loadMoreArticles} from "./ftools.js"


// Toggle the navigation bar
const topnavToggle = document.getElementById("topnavToggle-A");
topnavToggle.addEventListener("click", function() {
  const topnav = document.getElementById("topnav-A");
  if (topnav.className === "topnav") {
    topnav.classList.add("toggle");
  } else {
    topnav.className = "topnav";
  }
});

// Load More Functionality
let articles = document.querySelectorAll("article.badge");
loadMoreArticles(articles, 7);
