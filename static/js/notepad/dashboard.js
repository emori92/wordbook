
'user strict';


// 表示のオンオフをsessionStorageで保存する
if (sessionStorage.getItem('dashboard') === null) {
  sessionStorage.setItem('dashboard', 'wordbook');
}
// display wordbook
let active_id = sessionStorage.getItem('dashboard');

// 未ログイン時とログイン時のsessionを判定
if (active_id === 'wordbook') {
  let public = document.getElementById('wordbook');
  public.classList.remove('d-none');
} else {
  // 自分のdashboardでいいねをするとsessionがlikedになる。
  // likedのまま他のdashboardに移動すると表示されなくなるので、表示できるように変更
  let objectList = document.getElementById(active_id);
  if ( objectList === null) {
    const wordbook = document.getElementById('wordbook');
    wordbook.classList.remove('d-none');
  } else {
    objectList.classList.remove('d-none');
  }
}

// add or remove class
const changeDisplay = (id1, id2) => {
  // save session
  sessionStorage.setItem('dashboard', id1);
  // get element
  let element1 = document.getElementById(id1);
  let element2 = document.getElementById(id2);
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
