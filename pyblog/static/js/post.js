
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
