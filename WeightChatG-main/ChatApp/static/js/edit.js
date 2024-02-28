document.getElementById("edit-profile-form").addEventListener("submit", function(event) {
    event.preventDefault(); // デフォルトのフォーム送信をキャンセル

    // ポップアップを表示
    console.log("変更が保存されました");
    alert("変更が保存されました");

    // フォームを送信
    this.submit();
});



