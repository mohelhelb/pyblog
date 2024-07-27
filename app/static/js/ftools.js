// Function Tools

// Display/Hide Modal
export function displayModal(toggleModal, modal, cancelModal, targetForm) {
  if (toggleModal) {
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
  };
}


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

 static sortByDateCompFunc(post1, post2) { 
   let timeStamp1 = post1.getElementsByClassName("time-stamp")[0].innerText; 
   let timeStamp2 = post2.getElementsByClassName("time-stamp")[0].innerText;
   return timeStamp2 - timeStamp1;
 } 

 static sortByViewsCompFunc(post1, post2) { 
   let numViews1 = post1.getElementsByClassName("views")[0].innerText; 
   let numViews2 = post2.getElementsByClassName("views")[0].innerText;
   return numViews2 - numViews1;
 }

  static convertStampToLag(post) {
    let timeStamp = post.getElementsByClassName("time-stamp")[0].innerText;
    let minute = 60;
    let hour = 60 * 60;
    let day = 24 * 60 * 60;
    let month = 30 * 24 * 60 * 60;
    let year = 12 * 30 * 24 * 60 * 60;
    switch (true) {
      case 0 < timeStamp && timeStamp < 2 * minute:
        return "1 minute ago";
      case 2 * minute <= timeStamp && timeStamp < hour:
        return Math.floor(timeStamp / minute) + " minutes ago";
      case hour <= timeStamp && timeStamp < 2 * hour:
        return "1 hour ago";
      case 2 * hour <= timeStamp && timeStamp < day:
        return Math.floor(timeStamp / hour) + " hours ago";
      case day <= timeStamp && timeStamp < 2 * day:
        return "1 day ago";
      case 2 * day <= timeStamp && timeStamp < month:
        return Math.floor(timeStamp / day) + " days ago";
      case month <= timeStamp && timeStamp < 2 * month:
        return "1 month ago";
      case 2 * month <= timeStamp && timeStamp < year:
        return Math.floor(timeStamp / month) + " months ago";
      case year <= timeStamp && timeStamp < 2 * year:
        return "1 year ago";
      case 2 * year <= timeStamp:
        return Math.floor(timeStamp / year) + " years ago";
    }
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

  substituteStampForLag() {
    for (let i = 0; i < this.postElements.length; i++) {
      const timeLagElemnt = this.postElements[i].getElementsByClassName("lag")[0];
      timeLagElemnt.innerText = this.constructor.convertStampToLag(this.postElements[i]);
    }
  }

 loadMore(loadMoreButton) {
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
   this.postElements = this.replace(this.clone().sort(this.constructor.sortByDateCompFunc));
   if (reverse) {
     this.postElements = this.replace(this.clone().sort(this.constructor.sortByDateCompFunc).reverse());
   }
   if (this.currentPage === m + 1 & n != 0) {
     this.display(0, this.postElements.length - 1);
     return false;
   }
   this.display(0, this.currentPage * this.perPagePostElements - 1);
 }                     

 sortByViews() {
   let m = Math.floor(this.postElements.length / this.perPagePostElements);
   let n = this.postElements.length % this.perPagePostElements;
   this.hide();
   this.postElements = this.replace(this.clone().sort(this.constructor.sortByViewsCompFunc));
   if (this.currentPage === m + 1 & n != 0) {
     this.display(0, this.postElements.length - 1);
     return false;
   }
   this.display(0, this.currentPage * this.perPagePostElements - 1);
 }
}
