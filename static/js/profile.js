// Display/Hide the profile form //
const editProfileButton = document.getElementById("editProfileButton");
const cancelProfileButton = document.getElementById("cancelProfileButton"); 
const profileFormCard = document.getElementById("profileFormCard"); 
const profileForm = document.getElementById("profileForm");
editProfileButton.addEventListener("click", function(e) {
  profileFormCard.style.display = "block";
  this.style.display = "none";
});
cancelProfileButton.addEventListener("click", function(e) {
  // Reset all the form elements //
  profileForm.reset();

  profileFormCard.style.display = "none";
  editProfileButton.style.display = "inline-block";
  // Scroll to the top //
  window.scrollTo(0, 0);
}); 
