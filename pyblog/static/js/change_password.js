import {displayModal, outlineFieldDanger} from "./ftools.js"
             
// Outline fields with errors on focus  
const inputFields = document.querySelectorAll("form input:not([type='submit'])");
outlineFieldDanger(inputFields);

// Change password modal
const changePasswordToggle = document.querySelector(".forgot-password a");
const changePasswordModal = document.querySelector("#changePasswordModal"); 
const cancelChangePasswordModal = document.querySelector("#changePasswordModal button");  
const changePasswordForm = document.querySelector("#changePasswordModal form"); 
displayModal(changePasswordToggle, changePasswordModal, cancelChangePasswordModal, changePasswordForm); 
