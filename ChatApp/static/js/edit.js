document.getElementById("edit-profile-form").addEventListener("submit", function(event) {
    event.preventDefault(); // デフォルトのフォーム送信をキャンセル

    // ポップアップを表示
    console.log("変更が保存されました");
    alert("変更が保存されました");

    // フォームを送信
    this.submit();
});

// 公開ラジオボタンが選択された場合の処理
publicRadio.addEventListener("change", function() {
    if (this.checked) {
        console.log("公開が選択されました。");
        // 選択された場合の処理をここに追加する（必要に応じて）
    }
});

// 非公開ラジオボタンが選択された場合の処理
noPublicRadio.addEventListener("change", function() {
    if (this.checked) {
        console.log("非公開が選択されました。");
        // 選択された場合の処理をここに追加する（必要に応じて）
    }
});

