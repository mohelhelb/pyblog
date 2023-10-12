import {hasErrors, outlineFieldDanger, Post} from "./ftools.js"

// Display/Hide the profile form
const editProfileButton = document.getElementById("editProfileButton");
const cancelProfileButton = document.getElementById("cancelProfileButton"); 
const profileFormCard = document.getElementById("profileFormCard"); 
const profileForm = document.getElementById("profileForm");
editProfileButton.addEventListener("click", function() {
  profileFormCard.style.display = "block";
  this.style.display = "none";
});
cancelProfileButton.addEventListener("click", function() {
  // Reset all the form elements
  profileForm.reset();

  profileFormCard.style.display = "none";
  editProfileButton.style.display = "inline-block";
  // Scroll to the top
  window.scrollTo(0, 0);
}); 
// Display the profile form if it has errors
window.addEventListener("load", function() {
  if (hasErrors(profileForm)) {
    editProfileButton.click();
  }
}); 

// Display/Hide Modal
function displayModal(toggleModal, modal, cancelModal, targetForm) {
  toggleModal.addEventListener("click", function() {
    modal.style.display = "block"; 
    cancelModal.addEventListener("click", function() {
      targetForm.reset();
      modal.style.display = "none";
    }); 
    window.onclick = function(e) {
      if (e.target === modal) {
        modal.style.display = "none";
      }
    }
  });
}

// Delete Account Modal 
const deleteAccountToggle = document.querySelector(".account div:last-child .circle");
const deleteAccountModal = document.querySelector("#deleteAccountModal"); 
const cancelDeleteAccountModal = document.querySelector("#deleteAccountModal button");  
const deleteAccountForm = document.querySelector("#deleteAccountModal form"); 
displayModal(deleteAccountToggle, deleteAccountModal, cancelDeleteAccountModal, deleteAccountForm); 

// Outline fields with errors on focus  
const inputFields = document.querySelectorAll("form input:not([type='submit'])");
const textAreaField = document.querySelector("form textarea");
outlineFieldDanger(inputFields, textAreaField);

// Send the image form on image upload
const imageField = document.querySelector("#imageForm input[type='file']");
imageField.addEventListener("change", function() {
  const imageFormSubmitButton = document.querySelector("#imageForm input[type='submit']");
  imageFormSubmitButton.click();
});   

 
// Sorting Functionality: Hidden Posts
// Pending: Duplicate Code (See index.js)
const hiddenPostsNewestButton = document.querySelector("#myHiddenPosts .sort > div:first-child .circle"); 
const hiddenPostsOldestButton = document.querySelector("#myHiddenPosts .sort > div:last-child .circle"); 
const hiddenPostsSwitch = document.querySelector("#myHiddenPosts h3");
const hiddenPostElements = document.querySelectorAll("#myHiddenPosts .post");
if (hiddenPostElements.length) { 
  const hiddenPosts = new Post(hiddenPostElements);
  hiddenPosts.loadMore(); 
  hiddenPosts.sortByDate(); 
  hiddenPostsNewestButton.addEventListener("click", function() { 
    hiddenPostsSwitch.children[0].className = "fa-solid fa-arrow-up";
    hiddenPosts.sortByDate();
  }); 
  hiddenPostsOldestButton.addEventListener("click", function() {
    hiddenPostsSwitch.children[0].className = "fa-solid fa-arrow-down";
    hiddenPosts.sortByDate({reverse: true}); 
  }); 
};  

 
// Sorting Functionality: Released Posts
// Pending: Duplicate Code (See index.js)
const releasedposts = document.querySelector("#myReleasedPosts .sort > div:nth-child(2) .circle"); 
const releasedPostsOldestButton = document.querySelector("#myReleasedPosts .sort > div:nth-child(3) .circle"); 
const releasedPostsSwitch = document.querySelector("#myReleasedPosts h3");
const releasedPostElements = document.querySelectorAll("#myReleasedPosts .post");
if (releasedPostElements.length) { 
  const releasedPosts = new Post(releasedPostElements); 
  releasedPosts.loadMore(); 
  releasedPosts.sortByDate(); 
  releasedposts.addEventListener("click", function() { 
    releasedPostsSwitch.children[0].className = "fa-solid fa-arrow-up";
    releasedPosts.sortByDate();
  }); 
  releasedPostsOldestButton.addEventListener("click", function() {
    releasedPostsSwitch.children[0].className = "fa-solid fa-arrow-down";
    releasedPosts.sortByDate({reverse: true}); 
  });  
};


// Sorting Functionality: Bookmarks
// Pending: Duplicate Code (See index.js)
const bookmarksNewestButton = document.querySelector("#myBookmarks .sort > div:nth-child(2) .circle"); 
const bookmarksOldestButton = document.querySelector("#myBookmarks .sort > div:nth-child(3) .circle"); 
const bookmarksSwitch = document.querySelector("#myBookmarks h3");
const bookmarkElements = document.querySelectorAll("#myBookmarks .post");
const bookmarks = new Post(bookmarkElements);
bookmarks.loadMore(); 
bookmarks.sortByDate(); 
bookmarksNewestButton.addEventListener("click", function() { 
  bookmarksSwitch.children[0].className = "fa-solid fa-arrow-up";
  bookmarks.sortByDate();
}); 
bookmarksOldestButton.addEventListener("click", function() {
  bookmarksSwitch.children[0].className = "fa-solid fa-arrow-down";
  bookmarks.sortByDate({reverse: true}); 
});


// Dashboard
const myPostsButton = document.querySelector(".chart:first-of-type div:first-child .circle");
const myPosts = document.querySelector("#myPosts");
const myBookmarksButton = document.querySelector(".chart:first-of-type div:last-child .circle");
const myBookmarks = document.querySelector("#myBookmarks"); 
const followersButton = document.querySelector(".chart:nth-of-type(2) div:first-child .circle");
const followers = document.querySelector("#followers"); 
const followingButton = document.querySelector(".chart:nth-of-type(2) div:last-child .circle");
const following = document.querySelector("#following");
const myButtons = new Map([
  [myPostsButton, myPosts],
  [myBookmarksButton, myBookmarks],
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
        myButtons.get(btn).style.display = "none";
      };                 
    };
    this.style.outline = "3px solid rgba(0, 123, 255, 0.3)";
    this.style.border = "none";
    this.style.color = "#007bff";
    myButtons.get(this).style.display = "Block";
    myButtons.get(this).scrollIntoView({behavior: "smooth"});
  });
}; 

// Display posts by default.
window.addEventListener("load", function() {
  myPostsButton.click();
  this.scrollTo(0, 0);
}); 




