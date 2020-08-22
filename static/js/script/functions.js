
'user strict';


// add or remove class
const changeStyle2 = (sessionKey, id1, id2) => {
  // get element
  let elem1 = document.getElementById(id1);
  let elem2 = document.getElementById(id2);
  // change display
  elem1.classList.remove('d-none');
  elem2.classList.add('d-none');
  // save session
  sessionStorage.setItem(sessionKey, id1);
}

const changeStyle3 = (sessionKey, id1, id2, id3) => {
  // get element
  let elem1 = document.getElementById(id1);
  let elem2 = document.getElementById(id2);
  let elem3 = document.getElementById(id3);
  // change display
  elem1.classList.remove('d-none');
  elem2.classList.add('d-none');
  elem3.classList.add('d-none');
  // save session
  sessionStorage.setItem(sessionKey, id1);
}


// change display tab
const changeTabDisplay2 = (params) => {
  // parameter
  const key = params['sessionName'];
  const nowValue = sessionStorage.getItem(key);
  const initValue = params['sessionInit'];
  // 初回アクセス時はsessionを設定
  if (nowValue === null) {
    sessionStorage[key] = initValue;
  }
  // display wordbook
  let tab = document.getElementById(nowValue);
  tab.classList.remove('d-none');
  // btn
  let btn1 = document.getElementById(params['btnId1']);
  let btn2 = document.getElementById(params['btnId2']);
  // push btn
  if (btn1 && btn2) {
    btn1.addEventListener('click', () => { changeStyle2(key, params['tabId1'], params['tabId2']) });
    btn2.addEventListener('click', () => { changeStyle2(key, params['tabId2'], params['tabId1']) });
  }
}

const changeTabDisplay3 = (params) => {
  // parameter
  const key = params['sessionName'];
  const nowValue = sessionStorage.getItem(key);
  const initValue = params['sessionInit'];
  // 初回アクセス時はsessionを設定
  if (nowValue === null) {
    sessionStorage[key] = initValue;
  }
  // display wordbook
  let tab = document.getElementById(nowValue);
  tab.classList.remove('d-none');
  // btn
  let btn1 = document.getElementById(params['btnId1']);
  let btn2 = document.getElementById(params['btnId2']);
  let btn3 = document.getElementById(params['btnId3']);
  // push btn
  if (btn1 && btn2 && btn3) {
    btn1.addEventListener('click', () => { changeStyle3(key, params['tabId1'], params['tabId2'], params['tabId3']) });
    btn2.addEventListener('click', () => { changeStyle3(key, params['tabId2'], params['tabId1'], params['tabId3']) });
    btn3.addEventListener('click', () => { changeStyle3(key, params['tabId3'], params['tabId1'], params['tabId2']) });
  } else {
    btn1.addEventListener('click', () => { changeStyle2(key, params['tabId1'], params['tabId3']) });
    btn3.addEventListener('click', () => { changeStyle2(key, params['tabId3'], params['tabId1']) });
  }
}


// export
export { changeTabDisplay2, changeTabDisplay3 };
