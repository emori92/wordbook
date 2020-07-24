
'user strict';


// 表示のオンオフをsessionStorageで保存する
if (sessionStorage.getItem('myDashboard') === null) {
  sessionStorage.setItem('myDashboard', 'wordbook');
}
// display wordbook
let active_id = sessionStorage.getItem('myDashboard');
let wordbooks = document.getElementById(active_id);
// document.getElementById('public`').classList.remove('d-none');
wordbooks.classList.remove('d-none');

// add or remove class
const changeDisplay = (id1, id2) => {
  // get element
  let element1 = document.getElementById(id1);
  let element2 = document.getElementById(id2);
  // save session
  sessionStorage.setItem('myDashboard', id1);
  // change display
  element1.classList.remove('d-none');
  element2.classList.add('d-none');
}

// btn
let wordbook = document.getElementById('wordbook-btn');
let liked = document.getElementById('liked-btn');

// push btn
wordbook.addEventListener('click', () => { changeDisplay('wordbook', 'liked') });
liked.addEventListener('click', () => { changeDisplay('liked', 'wordbook') });
