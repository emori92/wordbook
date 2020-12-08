
'user strict';


// タブ表示の初期パラメータ
const tabSessions = {
  'search': 'wordbook',
  'ranking': 'star',
  'hot': 'wordbook',
  'dashboard': 'wordbook',
  'noteDetail': 'question'
}

// タブ表示のsessionを初期化
for (let key in tabSessions) {
  sessionStorage.setItem(key, tabSessions[key]);
}
