
'user strict';


// add or remove class
const addDisplayNone = (key, ...args) => {
  // edit display class
  for (let num in args) {
    if (num == 0) {  // (num === 0)とするとfalseになる
      document.getElementById(args[num]).classList.remove('d-none');
    } else {
      document.getElementById(args[num]).classList.add('d-none');
    }
  }
  // save session
  sessionStorage.setItem(key, args[0]);
}


// change display element
const changeTabDisplay = (params) => {
  // parameter
  const key = params['sessionName'];
  let session = sessionStorage.getItem(key);
  // 初回アクセス時はsessionを設定
  if (session === null) {
    session = params['id'][0];
  }
  // sessionとidが同じ要素を表示する
  const elemId = params['id'];
  elemId.forEach((id) => {
    if (id === session) {
      document.getElementById(id).classList.remove('d-none');
    }
  });
  // btn
  let btn1 = document.getElementById(elemId[0] + '-btn');
  let btn2 = document.getElementById(elemId[1] + '-btn');
  let btn3 = document.getElementById(elemId[2] + '-btn');
  // btnを押したら表示を切り替える
  if (btn1 && btn2 && btn3) {
    btn1.addEventListener('click', () => { addDisplayNone(key, elemId[0], elemId[1], elemId[2]) });
    btn2.addEventListener('click', () => { addDisplayNone(key, elemId[1], elemId[0], elemId[2]) });
    btn3.addEventListener('click', () => { addDisplayNone(key, elemId[2], elemId[0], elemId[1]) });
  } else if (btn1 && btn3) {
    btn1.addEventListener('click', () => { addDisplayNone(key, elemId[0], elemId[2]) });
    btn3.addEventListener('click', () => { addDisplayNone(key, elemId[2], elemId[0]) });
  } else if (btn1 && btn2) {
    btn1.addEventListener('click', () => { addDisplayNone(key, elemId[0], elemId[1]) });
    btn2.addEventListener('click', () => { addDisplayNone(key, elemId[1], elemId[0]) });
  }
}


// export
export { changeTabDisplay };
