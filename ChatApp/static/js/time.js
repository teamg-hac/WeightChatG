// 時間を表示する関数
function displayTime() {
    // 現在の日時を取得
    var now = new Date();
  
    // 時刻を取得
    var hours = now.getHours();
    var minutes = now.getMinutes();
    var seconds = now.getSeconds();
  
    // 0埋めして2桁にする
    hours = String(hours).padStart(2, '0');
    minutes = String(minutes).padStart(2, '0');
    seconds = String(seconds).padStart(2, '0');
  
    // 時刻を文字列に整形
    var timeString = hours + ':' + minutes + ':' + seconds;
  
    // HTML要素に時刻を表示
    document.getElementById('current-time').textContent = timeString;
  }
  
  // 定期的に時間を更新する関数
  function updateTime() {
    // 時間を表示
    displayTime();
  
    // 1秒ごとに時間を更新
    setInterval(displayTime, 1000);
  }
  
  // ページが読み込まれたときに実行
  document.addEventListener('DOMContentLoaded', function() {
    // 時間を更新
    updateTime();
  });
  