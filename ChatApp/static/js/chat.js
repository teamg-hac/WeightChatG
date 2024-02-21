const userInfoBar = document.getElementById('user-info-bar');
const userInfo = document.getElementById('user-info');

// ユーザー情報バーがクリックされたときに、ユーザー情報を切り替える
userInfoBar.addEventListener('click', () => {
    userInfo.classList.toggle('show');
});

document.getElementById("chatroom-form").addEventListener("submit", function(event) {
    // ダイアログメッセージを表示
    alert("チャットルームが作成されました！");

    // フォームをサブミットする（実際のアプリケーションでは、サーバーにフォームデータを送信するために必要）
    this.submit();
});