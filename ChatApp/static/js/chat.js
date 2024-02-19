const userInfoBar = document.getElementById('user-info-bar');
const userInfo = document.getElementById('user-info');

// ユーザー情報バーがクリックされたときに、ユーザー情報を切り替える
userInfoBar.addEventListener('click', () => {
    userInfo.classList.toggle('show');
});

document.getElementById("chatroom-form").addEventListener("submit", function(event) {
    // フォームの送信をキャンセル
    event.preventDefault();
    
    // 確認メッセージを表示し、ユーザーが「はい」を選択した場合のみフォームを送信
    if (confirm("このインストラクターとのチャットルームを作成してよろしいですか？")) {
        // フォームを送信
        this.submit();
        alert("チャットルームを作成しました！");
    }
});