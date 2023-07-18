
import {Post} from "./ftools.js" 

// Display trending posts
const trendingPostElements = [                    
  document.querySelector(".post:nth-of-type(1)"),  
  document.querySelector(".post:nth-of-type(2)"), 
  document.querySelector(".post:nth-of-type(3)"),
];
for (let i = 0; i < trendingPostElements.length; i++) {
  trendingPostElements[i].style.display = "block";
}

// Sorting Functionality
const newestButton = document.querySelector(".sort > div:nth-child(2) .circle"); 
const oldestButton = document.querySelector(".sort > div:nth-child(3) .circle"); 
const newestReleases = document.querySelector("#switchNewestOldest"); 
const postElements = document.querySelectorAll(".post:nth-of-type(3) ~ .post"); 
const posts = new Post(postElements);
posts.loadMore(); 
posts.sortByDate();
newestButton.addEventListener("click", function() { 
  newestReleases.children[0].className = "fa-solid fa-arrow-up";
  newestReleases.children[1].innerText = "Newest Releases"; 
  posts.sortByDate();
}); 
oldestButton.addEventListener("click", function() {
  newestReleases.children[0].className = "fa-solid fa-arrow-down";
  newestReleases.children[1].innerText = "Oldest Releases";
  posts.sortByDate({reverse: true}); 
}); 
