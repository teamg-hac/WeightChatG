// delete-button要素を取得
var deleteButton = document.getElementById("delete-button");

// ボタンがクリックされた時の処理を追加
deleteButton.addEventListener("click", function() {
    // ダイアログメッセージの表示
    var result = confirm("本当に削除しますか？");
    // 「はい」が選択された場合
    if (result) {
        // 削除しましたのメッセージの表示
        alert("削除しました");
    }
});
