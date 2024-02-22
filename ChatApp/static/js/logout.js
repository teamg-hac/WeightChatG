// ログアウトボタンのクリックイベントをリッスンして、ログアウトの確認ダイアログを表示する
document.getElementById("logout-button-side").addEventListener("click", function(event) {
    // デフォルトの動作をキャンセルする
    event.preventDefault();
    
    // 確認メッセージを表示し、ユーザーが「はい」を選択した場合のみログアウトを実行する
    if (confirm("ログアウトしますか？")) {
        // ログアウトの処理を記述（例えば、セッションをクリアするなど）
        alert("ログアウトしました！");
        // フォームをサブミットする
        this.parentElement.submit();
    }
});
