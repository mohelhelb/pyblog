
import {Post} from "./ftools.js"

// Sorting Functionality
const newestButton = document.querySelector(".sort > div:nth-child(2) .circle"); 
const oldestButton = document.querySelector(".sort > div:nth-child(3) .circle");
const postElements = document.querySelectorAll(".post"); 
const posts = new Post(postElements);
posts.loadMore(); 
posts.sortByDate();
newestButton.addEventListener("click", function() {
  posts.sortByDate();
}); 
oldestButton.addEventListener("click", function() {
  posts.sortByDate({reverse: true}); 
}); 

