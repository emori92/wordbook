
'user strict';


// btn
let wordbook = document.getElementById('wordbook-btn');
let recommender = document.getElementById('recommender-btn');

// add or remove class
const changeClass = (id1, id2) => {
  // get element
  let element1 = document.getElementById(id1);
  let element2 = document.getElementById(id2);
  // change class
  element1.classList.remove('d-none');
  element1.classList.add('d-flex');
  element2.classList.remove('d-flex');
  element2.classList.add('d-none');
}

// push btn
wordbook.addEventListener('click', () => { changeClass('wordbook', 'recommender') });
recommender.addEventListener('click', () => { changeClass('recommender', 'wordbook') });
