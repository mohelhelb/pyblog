
import {Post} from "./ftools.js" 

// Display trending posts
const trendingPostElements = document.querySelectorAll("#trendingPosts .post");
if (trendingPostElements.length) {
  const trendingPosts = new Post(trendingPostElements);
  trendingPosts.display(0, trendingPostElements.length - 1);
  trendingPosts.substituteStampForLag();
}

// Sorting Functionality
const postsTrendingButton = document.querySelector("#publicPosts .sort > div:first-child .circle");
const postsNewestButton = document.querySelector("#publicPosts .sort > div:nth-child(2) .circle"); 
const postsOldestButton = document.querySelector("#publicPosts .sort > div:nth-child(3) .circle"); 
const releases = document.querySelector("#publicPosts h3");
const postElements = document.querySelectorAll("#publicPosts .post"); 
if (postElements.length) { 
  const posts = new Post(postElements);
  const loadMoreButton = document.querySelector("#publicPosts .load-more .circle");
  posts.substituteStampForLag();
  posts.loadMore(loadMoreButton); 
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
