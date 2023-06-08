// Display/Hide the profile form //
const editProfileButton = document.getElementById("editProfileButton");
const cancelProfileButton = document.getElementById("cancelProfileButton");
const profileForm = document.getElementById("profileForm");
editProfileButton.addEventListener("click", function(e) {
  profileForm.style.display = "block";
  this.style.display = "none";
});
cancelProfileButton.addEventListener("click", function(e) {
  // Reset all the form elements //
  profileForm.reset();

  profileForm.style.display = "none";
  editProfileButton.style.display = "inline-block";
  // Scroll to the top //
  window.scrollTo(0, 0);
}); 
