
'user strict';


// add or remove class
const changeDisplay = (id1, id2, id3) => {
  // get element
  let element1 = document.getElementById(id1);
  let element2 = document.getElementById(id2);
  let element3 = document.getElementById(id3);
  // change display
  element1.classList.remove('d-none');
  element1.classList.add('d-flex');
  element2.classList.remove('d-flex');
  element2.classList.add('d-none');
  element3.classList.remove('d-flex');
  element3.classList.add('d-none');
  // change btn active
  // if (wordbook.classList.contains('active')) {
  //   wordbook.classList.remove('active');
  //   recommender.classList.add('active');
  // } else {
  //   recommender.classList.remove('active');
  //   wordbook.classList.add('active');
  // }
}

// btn
let wordbook = document.getElementById('wordbook-btn');
let follow = document.getElementById('follow-btn');
let recommender = document.getElementById('recommender-btn');

// push btn
wordbook.addEventListener('click', () => { changeDisplay('wordbook', 'follow', 'recommender') });
follow.addEventListener('click', () => { changeDisplay('follow', 'wordbook', 'recommender') });
recommender.addEventListener('click', () => { changeDisplay('recommender', 'wordbook', 'follow') });
