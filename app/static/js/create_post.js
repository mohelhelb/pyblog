import {outlineFieldDanger} from "./ftools.js"

// Outline fields with errors on focus  
const inputFields = document.querySelectorAll("form input[type='text']");
const textAreaField = document.querySelector("form textarea");
outlineFieldDanger(inputFields, textAreaField); 
