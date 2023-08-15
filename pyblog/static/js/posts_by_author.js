
import {Post} from "./ftools.js"

// Sorting Functionality
// const newestButton = document.querySelector(".sort > div:nth-child(2) .circle"); 
// const oldestButton = document.querySelector(".sort > div:nth-child(3) .circle");
// const postElements = document.querySelectorAll(".post"); 
// const posts = new Post(postElements);
// posts.loadMore(); 
// posts.sortByDate();
// newestButton.addEventListener("click", function() {
//   posts.sortByDate();
// }); 
// oldestButton.addEventListener("click", function() {
//   posts.sortByDate({reverse: true}); 
// }); 


// Sorting Functionality
// Pending: Duplicate Code (See index.js)
const newestButton = document.querySelector(".sort > div:nth-child(2) .circle"); 
const oldestButton = document.querySelector(".sort > div:nth-child(3) .circle"); 
const newestReleases = document.querySelector("#switchNewestOldest"); // Pending: Multiple elements with this id 
const postElements = document.querySelectorAll(".post"); 
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
