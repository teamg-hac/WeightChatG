// 削除ボタンのクリックイベントをリッスンして、削除アクションを実行する
var deleteButtons = document.querySelectorAll('.delete-button');
deleteButtons.forEach(function(button) {
    button.addEventListener('click', function(event) {
        event.preventDefault(); // デフォルトのイベントをキャンセル
        
        // ボタンがクリックされたときに実行するアクションをここに記述する
        var confirmation = confirm("チャットルームを削除しますか？");
        if (confirmation) {
            // 確認ダイアログでOKがクリックされた場合、フォームを送信する
            button.parentElement.submit();
        }
    });
});

