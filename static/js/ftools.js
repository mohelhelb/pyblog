// Function Tools


// Display a selected range of articles
function displayArticlesFromTo(articles, start, end) {
  for (let j = start; j <= end; j++) {
    articles[j].style.display = "block";
  }
}


// Load more articles on mouse-clicking
export function loadMoreArticles(articles, perPageNumArticles) {
  let loadMoreButton = document.querySelector(".load-more button");
  let totalNumArticles = articles.length;
  let division = totalNumArticles / perPageNumArticles;
  let floorDivision = Math.floor(totalNumArticles / perPageNumArticles);
  let remainder = totalNumArticles % perPageNumArticles;
  let start = 0;
  let end = 0;
  let i = 1;
  if (!division) {
    return false;
  } else if (division > 0 && division <= 1) {
    start = 0;
    end = totalNumArticles - 1; // arr = ["a", "b", "c"] and end = arr.length - 1 --> arr[end] = "c"
    displayArticlesFromTo(articles, start, end);
    return false;
  }
  start = 0;
  end = perPageNumArticles - 1;
  displayArticlesFromTo(articles, start, end);
  loadMoreButton.style.display = "inline-block";
  loadMoreButton.addEventListener("click", function() {
    i++;
    if ((i === floorDivision + 1) && remainder) {
      // Index of first article on page k: (k - 1) * perPageNumArticles
      // Index of last article on page k: k * perPageNumArticles - 1
      start = floorDivision * perPageNumArticles; 
      end = totalNumArticles - 1;
      displayArticlesFromTo(articles, start, end);
      this.style.display = "none";
      return false;
    } else if ((i === floorDivision) && !remainder) {
      start = (floorDivision - 1) * perPageNumArticles;
      end = (floorDivision * perPageNumArticles) - 1;
      displayArticlesFromTo(articles, start, end);
      this.style.display = "none";
      return false;
    }
    start = (i - 1) * perPageNumArticles;
    end = (i * perPageNumArticles) - 1;
    displayArticlesFromTo(articles, start, end);
  });
}

