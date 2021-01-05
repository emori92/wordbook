
'user strict';

import { changeTabDisplay } from '../script/functions.js';


// function parameter
const noteDetailParameter = {
  'sessionName': 'noteDetail',
  'idList': ['question', 'review']
}

// get answer and hint class
let answers = document.querySelectorAll('.answer-btn');
let hints = document.querySelectorAll('.hint-btn');

// show answer, hint
const showText = (elemList, elemClass) => {
  // for loop elementList
  for (let i = 0; i < elemList.length; i++) {
    // click event
    elemList[i].addEventListener('click', () => {
      // get element
      let elem = elemList[i].parentElement.parentElement.parentElement.querySelector(elemClass);
      // add or remove 'display: none'
      if (elem.classList.contains('d-none')) {
        elem.classList.remove('d-none');
      } else {
        elem.classList.add('d-none');
      }
    });
  }
}

// execute functions
changeTabDisplay(noteDetailParameter);
showText(answers, '.answer');
showText(hints, '.hint');
