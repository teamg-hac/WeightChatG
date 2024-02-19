document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector("form");
  
    form.addEventListener("submit", function(event) {
      event.preventDefault(); // フォームのデフォルトの送信をキャンセル
  
      // ここにフォームの送信処理を追加する（例：サーバーに送信するなど）
  
      // ポップアップを表示する
      alert("ログインしました！");
    });
  });
  
// ログアウトボタンのクリックイベント
document.getElementById("logout-button").addEventListener("click", function() {
  // 確認メッセージを表示し、ユーザーが「はい」を選択した場合のみログアウト
  if (confirm("ログアウトしますか？")) {
      alert("ログアウトしました！");
      // ログアウトの処理を記述（例えば、セッションをクリアするなど）
  }
});
