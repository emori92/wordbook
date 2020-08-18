
'user strict';


// change display tab
const changeTabDisplay = (params) => {
  // タブの表示をsessionStorageで保存する
  const sessionKey = params['sessionName'];
  const sessionName = sessionStorage.getItem(sessionKey);
  if (sessionName === null) {
    sessionStorage[params['sessionName']] = params['sessionValue'];
  }
  // display wordbook
  let element = document.getElementById(sessionName);
  element.classList.remove('d-none');

  // add or remove class
  const changeDisplay = (id1, id2) => {
    // get element
    let element1 = document.getElementById(id1);
    let element2 = document.getElementById(id2);
    // change display
    element1.classList.remove('d-none');
    element2.classList.add('d-none');
    // save session
    sessionStorage.setItem(params['sessionName'], id1);
  }

  // btn
  let btn1 = document.getElementById(params['btnId1']);
  let btn2 = document.getElementById(params['btnId2']);

  // push btn
  if (btn1 && btn2) {
    btn1.addEventListener('click', () => { changeDisplay(params['btnValue1'], params['btnValue2']) });
    btn2.addEventListener('click', () => { changeDisplay(params['btnValue2'], params['btnValue1']) });
  }
}


// export
export {changeTabDisplay};
