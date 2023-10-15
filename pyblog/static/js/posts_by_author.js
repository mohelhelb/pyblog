
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


// Sorting Functionality: Posts
// Pending: Duplicate Code (See index.js) 
const postsTrendingButton = document.querySelector("#myPosts .sort > div:first-child .circle"); 
const postsNewestButton = document.querySelector("#myPosts .sort > div:nth-child(2) .circle"); 
const postsOldestButton = document.querySelector("#myPosts .sort > div:nth-child(3) .circle"); 
const releases = document.querySelector("#myPosts h3");
const postElements = document.querySelectorAll("#myPosts .post");
if (postElements.length) {
  const posts = new Post(postElements);
  posts.loadMore(); 
  posts.sortByDate();  
  postsTrendingButton.addEventListener("click", function() { 
    releases.children[0].className = "fa-solid fa-arrow-trend-up";
    releases.children[1].innerText = "Trending Releases";
    posts.sortByViews();
  }); 
  postsNewestButton.addEventListener("click", function() { 
    releases.children[0].className = "fa-solid fa-arrow-up";
    releases.children[1].innerText = "Newest Releases";
    posts.sortByDate();
  }); 
  postsOldestButton.addEventListener("click", function() {
    releases.children[0].className = "fa-solid fa-arrow-down"; 
    releases.children[1].innerText = "Oldest Releases"; 
    posts.sortByDate({reverse: true}); 
  }); 
};

// Dashboard
const myPostsButton = document.querySelector(".chart div:first-child .circle");
const myPosts = document.querySelector("#myPosts");
const followersButton = document.querySelector(".chart div:nth-of-type(2) .circle");
const followers = document.querySelector("#followers"); 
const followingButton = document.querySelector(".chart div:last-child .circle");
const following = document.querySelector("#following");
const myButtons = new Map([
  [myPostsButton, myPosts],
  [followersButton, followers],
  [followingButton, following]
]);
for (const button of myButtons.keys()) {
  button.addEventListener("click", function() {
    for (const btn of myButtons.keys()) {
      if (btn != this) {
        btn.style.outline = "none";
        btn.style.border = "1px solid #ddd";
        btn.style.color = "#666";
        if (myButtons.get(btn)) {
          myButtons.get(btn).style.display = "none";
        };
      };                 
    };
    this.style.outline = "3px solid rgba(0, 123, 255, 0.3)";
    this.style.border = "none";
    this.style.color = "#007bff";
    if (myButtons.get(this)) { 
      myButtons.get(this).style.display = "Block";
      myButtons.get(this).scrollIntoView({behavior: "smooth"}); 
    };
  });
}; 

// Display posts by default.
window.addEventListener("load", function() {
  myPostsButton.click();
  this.scrollTo(0, 0);
});               


