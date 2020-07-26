
'user strict';


// タブの表示をsessionStorageで保存する
if (sessionStorage.getItem('ranking') === null) {
  sessionStorage.setItem('ranking', 'star');
}
// display wordbook
let active_id = sessionStorage.getItem('ranking');
let wordbooks = document.getElementById(active_id);
wordbooks.classList.remove('d-none');

// add or remove class
const changeDisplay = (id1, id2) => {
  // get element
  let element1 = document.getElementById(id1);
  let element2 = document.getElementById(id2);
  // change display
  element1.classList.remove('d-none');
  element2.classList.add('d-none');
  // save session
  sessionStorage.setItem('ranking', id1);
}

// btn
let star = document.getElementById('star-btn');
let user = document.getElementById('user-btn');

// push btn
star.addEventListener('click', () => { changeDisplay('star', 'user') });
user.addEventListener('click', () => { changeDisplay('user', 'star') });

// ranking num
const print = c => console.log(c);

let rankNum = [];
for (let i = 1; i <= 40; i++) {
  rankNum.push(i);
}
