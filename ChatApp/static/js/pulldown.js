document.getElementById("spanSelect").addEventListener("change", function() {
    const selectedValue = this.value;
    // 選択された値をURLのクエリパラメータに設定してページをリロードする
    const url = new URL(window.location.href);
    url.searchParams.set('span', selectedValue);
    url.searchParams.set("graph", 1);
    window.location.href = url.toString();
});