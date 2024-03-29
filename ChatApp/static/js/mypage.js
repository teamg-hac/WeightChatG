//体重が入力されたとき
function submitWeight(event) {
    event.preventDefault(); // デフォルトのフォーム送信をキャンセル
    
    const weightInput = document.getElementById("weight-input");
    const newWeight = weightInput.value.trim();


    const confirmMessage = `本日の体重を ${newWeight} kg に更新します。よろしいですか？`;
    if (confirm(confirmMessage)) {
        alert("体重を更新しました。");
        // フォームを送信
        event.target.closest('form').submit();
    }
}



// 退会ボタンがクリックされたときの処理

document.getElementById("delete-button").addEventListener("click", function(event) {
    // デフォルトのイベントをキャンセル
    event.preventDefault();

    // 本当に退会しますか？の確認メッセージを表示
    if (confirm("本当に退会しますか？")) {
        // ここで退会処理を行う
        console.log("ユーザーが退会しました。");
        // フォームを送信
        this.closest('form').submit();
    }
});


/*
// HTMLからhidden要素を取得し、その値をJavaScriptの変数に代入する
var userPassword = document.getElementById('userPassword').value;
console.log(userPassword); // コンソールに表示される: 実際のパスワード

document.querySelector('.delete-button').addEventListener('click', function() {
    // 本当に退会しますか？の確認メッセージを表示
    if (confirm("本当に退会しますか？")) {
        // パスワード入力用のプロンプトを表示し、入力されたパスワードを取得
        var password = prompt("パスワードを入力してください:", "");

        // パスワードが入力された場合の処理
        if (password !== null && password !== "") {
            // SHA-256ハッシュを計算
            var hashedPassword = CryptoJS.SHA256(password).toString(CryptoJS.enc.Hex);

            // ハッシュ値をコンソールに表示
            console.log("SHA-256ハッシュ:", hashedPassword);

            // ハッシュ化されたパスワードとユーザーパスワードのハッシュ値を比較
            if (hashedPassword === hashedUserIdpass) { // ハッシュ値を比較
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
*/