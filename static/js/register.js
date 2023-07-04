import {outlineFieldDanger} from "./ftools.js"

// Outline fields with errors on focus  
const inputFields = document.querySelectorAll("form input:not([type='submit'])");
const textAreaField = document.querySelector("form textarea");
outlineFieldDanger(inputFields, textAreaField);
