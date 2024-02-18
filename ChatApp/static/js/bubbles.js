window.onload = function() {
    var canvas = document.getElementById('bubbles');
    var ctx = canvas.getContext('2d');
    
    // シャボン玉を描画する関数
    function draw() {
        // 描画コードをここに記述する
    }
    
    // シャボン玉を最初の3秒間だけ描画する
    draw();
    setTimeout(function() {
        // 3秒後にシャボン玉を消す
        ctx.clearRect(0, 0, canvas.width, canvas.height);
    }, 3000);
};
