// Code Snippets

// Circular Indexing
// (i j k): (0 1 2) --> ... --> (10 11 0) --> (11 1 2)
function nextTwo(hour) {
  const clock = [
    "1 o'clock",          
    "2 o'clock", 
    "3 o'clock", 
    "4 o'clock", 
    "5 o'clock", 
    "6 o'clock", 
    "7 o'clock", 
    "8 o'clock", 
    "9 o'clock", 
    "10 o'clock", 
    "11 o'clock", 
    "12 o'clock"
  ]
  for (let i = 0; i < clock.length; i++) {
    let j = i + 1;
    j === 12 ? j = 0 : j = j;
    let k = j + 1;
    k === 12 ? k = 0 : k = k;
    if (hour === clock[i]) {
      console.log(clock[j]);
      console.log(clock[k]);
    }
  }
}

nextTwo("12 o'clock");
