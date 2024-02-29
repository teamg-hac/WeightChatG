const userInfoBar = document.getElementById('user-info-bar');
const userInfo = document.getElementById('user-info');

// ユーザー情報バーがクリックされたときに、ユーザー情報を切り替える
userInfoBar.addEventListener('click', () => {
    userInfo.classList.toggle('show');
});