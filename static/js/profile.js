import {outlineFieldDanger, hasErrors} from "./ftools.js"

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




