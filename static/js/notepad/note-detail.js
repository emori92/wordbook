
'user strict';


// hintとanswerを表示する関数
let showText = (elemId) => {

  // 表示の処理
  let changeDisplay = (text) => {
    if (text.classList.contains('d-none')) {
      text.classList.remove('d-none');
    } else {
      text.classList.add('d-none');
    }
  }

  // hintとanswerの判別
  if (elemId.slice(0, 4) === 'hint') {
    let text = document.getElementById(`hint-${elemId.slice(-1)}`);
    changeDisplay(text);
  } else {
    let text = document.getElementById(`answer-${elemId.slice(-1)}`);
    changeDisplay(text);
  }
}
