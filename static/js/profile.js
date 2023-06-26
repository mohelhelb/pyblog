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

// Display/Hide Modal
function displayModal(toggleModal, modal, cancelModal, targetForm) {
  toggleModal.addEventListener("click", function() {
    modal.style.display = "block";
  });
  cancelModal.addEventListener("click", function() {
    targetForm.reset();
    modal.style.display = "none";
  });
}
 
// Change Password Modal
const changePasswordToggle = document.querySelector(".account div:first-child .circle"); 
changePasswordToggle.addEventListener("click", function () {
  const changePasswordModal = document.querySelector("#changePasswordModal"); 
  const cancelChangePasswordModal = document.querySelector("#changePasswordModal button"); 
  changePasswordModal.style.display = "block";
  cancelChangePasswordModal.addEventListener("click", function() {  
    const changePasswordForm = document.querySelector("#changePasswordModal form");
    changePasswordForm.reset();
    changePasswordModal.style.display = "none";
  });
  window.onclick = function(e) {
    if (e.target === changePasswordModal) {
      changePasswordModal.style.display = "none";
    }
  }
});

// Delete Account Modal 
const deleteAccountToggle = document.querySelector(".account div:last-child .circle"); 
deleteAccountToggle.addEventListener("click", function () {
  const deleteAccountModal = document.querySelector("#deleteAccountModal"); 
  const cancelDeleteAccountModal = document.querySelector("#deleteAccountModal button"); 
  deleteAccountModal.style.display = "block";
  cancelDeleteAccountModal.addEventListener("click", function() {  
    const deleteAccountForm = document.querySelector("#deleteAccountModal form"); 
    deleteAccountForm.reset();
    deleteAccountModal.style.display = "none";
  });
  window.onclick = function(e) {
    if (e.target === deleteAccountModal) {
      deleteAccountModal.style.display = "none";
    }
  }
}); 



