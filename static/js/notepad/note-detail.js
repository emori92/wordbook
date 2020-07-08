
'user strict';


// 実行
let answers = document.querySelectorAll('.answer-btn');
let hints = document.querySelectorAll('.hint-btn');


// 表示処理
const showText = (elemList, elemClass) => {

  for (let i = 0; i < elemList.length; i++) {
    // click event
    elemList[i].addEventListener('click', () => {
      // get elem
      let elem = elemList[i].parentElement.parentElement.parentElement.querySelector(elemClass);
      // display: none の削除、追加
      if (elem.classList.contains('d-none')) {
        elem.classList.remove('d-none');
      } else {
        elem.classList.add('d-none');
      }
    });
  }
}

showText(answers, '.answer');
showText(hints, '.hint');
