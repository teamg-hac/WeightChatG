document.getElementById("chatroom-form").addEventListener("submit", function(event) {
    // ダイアログメッセージを表示
    alert("チャットルームが作成されました！");

    // フォームをサブミットする（実際のアプリケーションでは、サーバーにフォームデータを送信するために必要）
    this.submit();
});