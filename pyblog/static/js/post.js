import {displayModal} from "./ftools.js"

// Delete Post Modal 
const deletePostToggle = document.querySelector(".edit-hide-delete .delete");
const deletePostModal = document.querySelector("#deletePostModal"); 
const cancelDeletePostModal = document.querySelector("#deletePostModal button");  
const deletePostForm = document.querySelector("#deletePostModal form"); 
displayModal(deletePostToggle, deletePostModal, cancelDeletePostModal, deletePostForm); 
