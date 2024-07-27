import {outlineFieldDanger} from "./ftools.js"
             
// Outline fields with errors on focus  
const inputFields = document.querySelectorAll("form input:not([type='submit'])");
outlineFieldDanger(inputFields);
