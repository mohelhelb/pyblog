// Function Tools


// Display a selected range of articles
function displayArticlesFromTo(articles, start, end) {
  for (let j = start; j <= end; j++) {
    articles[j].style.display = "block";
  }
}


// Outline fields with errors on focus
export function outlineFieldDanger(inputFields, textAreaField) {
  for (let i = 0; i < inputFields.length; i++) {
    if (inputFields[i].className === "field-danger") { 
      inputFields[i].addEventListener("focusin", function() {
        this.style.outline = "3px solid rgba(255, 102, 102, 0.3)";
        this.style.borderColor = "rgba(255, 102, 102, 0.5)";
      }); 
      inputFields[i].addEventListener("focusout", function() {
        this.style.outline = "none";
      });
    }
  }
  try {
    if (textAreaField.className === "field-danger") { 
      textAreaField.addEventListener("focusin", function() {
        this.style.outline = "3px solid rgba(255, 102, 102, 0.3)";
        this.style.borderColor = "rgba(255, 102, 102, 0.5)";
      }); 
      textAreaField.addEventListener("focusout", function() {
        this.style.outline = "none";
      });
    } 
  } catch (err) {
      // pass
    } 
}

// Determine if a form has errors
export function hasErrors(form) {
  if (form.getElementsByClassName("field-danger").length != 0) {
    return true;
  }
  return false;
}

// Classes

// Sorting/Load More Functionalities
export class Post {

 currentPage = 1;
 perPagePostElements = 3;

 static comparisonFunction(post1, post2) { 
   let dateString1 = post1.getElementsByClassName("date")[0].innerText; 
   let dateString2 = post2.getElementsByClassName("date")[0].innerText;
   const date1 = new Date(dateString1);
   const date2 = new Date(dateString2);
   return date2 - date1;
 }

 constructor(postElements) {
   this.postElements = Array.from(postElements);
 }

 clone() {
   const clonePostElements = [];
   for (let i = 0; i < this.postElements.length; i++) {
     clonePostElements.push(this.postElements[i].cloneNode(true));
   }
   return clonePostElements;
 }

 display(start, end) {
   for (let i = start; i <= end; i++) {
     this.postElements[i].style.display = "block";
   }
 }  

 hide() {
   for (let i = 0; i < this.postElements.length; i++) {
     if (this.postElements[i].style.display === "none") {
       break;
     }
     this.postElements[i].style.display = "none";
   }
 }

 replace(newPostElements) {
   for (let i = 0; i < this.postElements.length; i++) {
     this.postElements[i].replaceWith(newPostElements[i]);
   }
   return newPostElements;
 }

 loadMore() {
   const loadMoreButton = document.querySelector(".load-more .circle");
   let m = Math.floor(this.postElements.length / this.perPagePostElements);
   let n = this.postElements.length % this.perPagePostElements;
   if (this.postElements.length === 0) {
     return false;
   } else if (this.postElements.length <= this.perPagePostElements) {
     // arr = ["a", "b", "c"] and end = arr.length - 1 --> arr[end] = "c"
     this.display(0, this.postElements.length - 1);
     return false;
   }
   this.display(0, this.perPagePostElements - 1);
   loadMoreButton.style.display = "inline-block";
   var that = this;
   loadMoreButton.addEventListener("click", function() {
     that.currentPage++;      
     if (that.currentPage === m + 1 && n != 0) {
       // Index of first post on page k: (k - 1) * that.perPagePostElements 
       // Index of last post on page k: k * that.perPagePostElements - 1
       that.display(m * that.perPagePostElements, that.postElements.length - 1);
       this.style.display = "none";
       return false;
     } else if ((that.currentPage === m) && !n) {
       that.display((m - 1) * that.perPagePostElements, (m * that.perPagePostElements) - 1);
       this.style.display = "none";
       return false;
     }
     that.display((that.currentPage - 1) * that.perPagePostElements, (that.currentPage * that.perPagePostElements) - 1);
   });
 }                     

 sortByDate({reverse=false}={}) {
   let m = Math.floor(this.postElements.length / this.perPagePostElements);
   let n = this.postElements.length % this.perPagePostElements;
   this.hide();
   this.postElements = this.replace(this.clone().sort(this.constructor.comparisonFunction));
   if (reverse) {
     this.postElements = this.replace(this.clone().sort(this.constructor.comparisonFunction).reverse());
   }
   if (this.currentPage === m + 1 & n != 0) {
     this.display(0, this.postElements.length - 1);
     return false;
   }
   this.display(0, this.currentPage * this.perPagePostElements - 1);
 }
}
