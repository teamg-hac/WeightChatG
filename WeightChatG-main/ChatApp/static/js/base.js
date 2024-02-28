// DOMContentLoaded イベントが発生したときに実行される関数を定義
document.addEventListener("DOMContentLoaded", function() {
    // メニューボタン、サイドバー、閉じるボタンの要素を取得
    const menuButton = document.getElementById("menu-button");
    const sidebar = document.getElementById("sidebar");
    const closeButton = document.getElementById("close-button");

    // メニューボタンがクリックされたときの処理を定義
    menuButton.addEventListener("click", function() {
        // サイドバーの右側からの位置を取得
        const sidebarRight = parseInt(window.getComputedStyle(sidebar).getPropertyValue("right"));
        // サイドバーが右側に非表示の場合は表示し、表示されている場合は非表示にする
        if (sidebarRight < 0) {
            // サイドバーを表示するために右側からの位置を0に設定
            sidebar.style.right = "0";
            // 閉じている状態から開く場合、openクラスを追加してサイドバーを開く
            sidebar.classList.add("open");

        } else {
            // サイドバーを非表示にするために右側からの位置を-250pxに設定
            sidebar.style.right = "-250px";
            // 開いている状態から閉じる場合、openクラスを削除してサイドバーを閉じる
            sidebar.classList.remove("open");
        }
    });

    // 閉じるボタンがクリックされたときの処理を定義
    closeButton.addEventListener("click", function() {
        // サイドバーを非表示にするために右側からの位置を-250pxに設定
        sidebar.style.right = "-250px";
        // 閉じるボタンがクリックされた場合、openクラスを削除してサイドバーを閉じる
        sidebar.classList.remove("open");

    });
});
