// 退会ボタンがクリックされたときの処理
document.querySelector('.delete-button').addEventListener('click', function() {
    // 本当に退会しますか？の確認メッセージを表示
    if (confirm("本当に退会しますか？")) {
        // パスワード入力用のプロンプトを表示し、入力されたパスワードを取得
        var password = prompt("パスワードを入力してください:", "");
        
        // パスワードが入力された場合の処理
        if (password !== null && password !== "") {
            // パスワードが正しいかどうかをチェック（ここでは簡単なダミーパスワード "password" としています）
            if (password === "password") {
                // 正しいパスワードが入力された場合の処理
                // ここで退会処理を実行するなどの操作を行う
                console.log("ユーザーが退会しました。");
            } else {
                // パスワードが間違っている場合の処理
                alert("パスワードが間違っています。");
            }
        } else {
            // パスワードが入力されなかった場合の処理
            alert("パスワードが入力されていません。");
        }
    }
});
