
'user strict';


// add or remove class
const changeDisplay = (id1, id2) => {
  // get element
  let element1 = document.getElementById(id1);
  let element2 = document.getElementById(id2);
  // change display
  element1.classList.remove('d-none');
  element1.classList.add('d-flex');
  element2.classList.remove('d-flex');
  element2.classList.add('d-none');
}

// btn
let star = document.getElementById('star-btn');
let user = document.getElementById('user-btn');

// push btn
star.addEventListener('click', () => { changeDisplay('star', 'user') });
user.addEventListener('click', () => { changeDisplay('user', 'star') });
