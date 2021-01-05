
'user strict';


// add or remove class
const addDisplayNone = (sessionName, ...args) => {
  // edit display class
  for (let num in args) {
    if (num == 0) {  // (num === 0)とするとfalseになる
      document.getElementById(args[num]).classList.remove('d-none');
    } else {
      document.getElementById(args[num]).classList.add('d-none');
    }
  }
  // update session
  sessionStorage.setItem(sessionName, args[0]);
}


// change display element
const changeTabDisplay = (params) => {
  // get element id to display
  const sessionName = params['sessionName'];
  let displayId = sessionStorage.getItem(sessionName);
  const defaultId = params['idList'][0]
  // 初回アクセス時はsessionを設定
  if (displayId === null) {
    displayId = defaultId;
  }
  // idの配列を取得
  const idList = params['idList'];
  // sessionとidが同じ要素を表示する
  idList.forEach((id) => {
    const elem = document.getElementById(id);
    if (id === displayId) {
      // ログインユーザ以外のdashboardを表示
      if (elem === null) {
        // sessionを更新
        sessionStorage.setItem(sessionName, defaultId);
        // デフォルトのdashboardを表示
        document.getElementById(defaultId).classList.remove('d-none');
      // ログインユーザのdashboardを表示
      } else {
        document.getElementById(displayId).classList.remove('d-none');
      }
    }
  });
  // btn
  let btn1 = document.getElementById(idList[0] + '-btn');
  let btn2 = document.getElementById(idList[1] + '-btn');
  let btn3 = document.getElementById(idList[2] + '-btn');
  // btnを押したら表示を切り替える
  if (btn1 && btn2 && btn3) {
    btn1.addEventListener('click', () => { addDisplayNone(sessionName, idList[0], idList[1], idList[2]) });
    btn2.addEventListener('click', () => { addDisplayNone(sessionName, idList[1], idList[0], idList[2]) });
    btn3.addEventListener('click', () => { addDisplayNone(sessionName, idList[2], idList[0], idList[1]) });
  } else if (btn1 && btn3) {
    btn1.addEventListener('click', () => { addDisplayNone(sessionName, idList[0], idList[2]) });
    btn3.addEventListener('click', () => { addDisplayNone(sessionName, idList[2], idList[0]) });
  } else if (btn1 && btn2) {
    btn1.addEventListener('click', () => { addDisplayNone(sessionName, idList[0], idList[1]) });
    btn2.addEventListener('click', () => { addDisplayNone(sessionName, idList[1], idList[0]) });
  }
}


// export
export { changeTabDisplay };
