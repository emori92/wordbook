'user strict';


// hintとanswerを表示する関数
function showText(type) {

  // idの最後の一文字を取得
  let num = type.slice(-1);

  // 表示の処理
  function changeDisplay(text) {
    if (text.classList.contains('question-active')) {
      text.classList.remove('question-active');
      text.classList.add('question-not-active');
    } else {
      text.classList.remove('question-not-active');
      text.classList.add('question-active');
    }
  }

  // hintとanswerの判別
  if (type.slice(0, 4) === 'hint') {
    let text = document.getElementById(`hint-${num}`);
    changeDisplay(text);
  } else {
    let text = document.getElementById(`answer-${num}`);
    changeDisplay(text);
  }
}