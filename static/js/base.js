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


// Sorting Functionality
const sortToggle = document.querySelectorAll(".sort-toggle");
for (let i = 0; i < sortToggle.length; i++) {
  const sortMenu = sortToggle[i].nextElementSibling;
  const sortButton = sortToggle[i].getElementsByClassName("circle")[0];
  const sortIcon = sortButton.getElementsByTagName("i")[0];
  sortButton.addEventListener("click", function() {
    if (sortMenu.style.display === "block") {
      sortMenu.style.display = "none"; 
      sortIcon.className = "fa-solid fa-angles-down"; 
      return false;
    }
    sortMenu.style.display = "block";
    sortIcon.className = "fa-solid fa-angles-up";
  });
}


// Load More Functionality
let articles = document.querySelectorAll("article.badge");
loadMoreArticles(articles, 7);
