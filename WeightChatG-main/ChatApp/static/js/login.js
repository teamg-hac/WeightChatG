document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector("form");
  
    form.addEventListener("submit", function(event) {
      event.preventDefault(); // フォームのデフォルトの送信をキャンセル
  
      // ここにフォームの送信処理を追加する（例：サーバーに送信するなど）
  
      // ポップアップを表示する
      alert("ログインしました！");
    });
  });
  

