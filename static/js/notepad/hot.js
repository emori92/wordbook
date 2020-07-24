
'user strict';


// 表示のオンオフをsessionStorageで保存する
if (sessionStorage.getItem('hot') === null) {
  sessionStorage.setItem('hot', 'wordbook');
}
// display wordbook
let active_id = sessionStorage.getItem('hot');
let wordbooks = document.getElementById(active_id);
wordbooks.classList.remove('d-none');

// add or remove class
const changeDisplay = (id1, id2, id3) => {
  // get element
  let element1 = document.getElementById(id1);
  let element2 = document.getElementById(id2);
  let element3 = document.getElementById(id3);
  // save session
  sessionStorage.setItem('hot', id1);
  // change display
  element1.classList.remove('d-none');
  element2.classList.add('d-none');
  element3.classList.add('d-none');
}

// btn
let wordbook = document.getElementById('wordbook-btn');
let follow = document.getElementById('follow-btn');
let recommender = document.getElementById('recommender-btn');

// push btn
wordbook.addEventListener('click', () => { changeDisplay('wordbook', 'follow', 'recommender') });
recommender.addEventListener('click', () => { changeDisplay('recommender', 'wordbook', 'follow') });
follow.addEventListener('click', () => { changeDisplay('follow', 'wordbook', 'recommender') });
