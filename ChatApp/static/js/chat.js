const userInfoBar = document.getElementById('user-info-bar');
const userInfo = document.getElementById('user-info');

// ユーザー情報バーがクリックされたときに、ユーザー情報を切り替える
userInfoBar.addEventListener('click', () => {
    userInfo.classList.toggle('show');
});


function validateMessage() {
    const messageInput = document.getElementById("message-input");
    const message = messageInput.value.trim();

    // メッセージが空白であるかどうかをチェック
    if (message === "") {
        alert("メッセージが空白です。");
        return false; // フォームの送信をキャンセル
    }

    return true; // フォームを送信
}