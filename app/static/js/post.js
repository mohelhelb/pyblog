import {displayModal, Post} from "./ftools.js"

// Pending
const postElements = document.querySelectorAll("#singlePost");
if (postElements.length) {
  const post = new Post(postElements);
  post.display(0, 0);
  post.substituteStampForLag();
}

// Delete Post Modal 
const deletePostToggle = document.querySelector(".edit-hide-delete .delete");
const deletePostModal = document.querySelector("#deletePostModal"); 
const cancelDeletePostModal = document.querySelector("#deletePostModal button");  
const deletePostForm = document.querySelector("#deletePostModal form"); 
displayModal(deletePostToggle, deletePostModal, cancelDeletePostModal, deletePostForm); 
