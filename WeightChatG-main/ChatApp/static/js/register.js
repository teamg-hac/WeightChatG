document.addEventListener("DOMContentLoaded", function() {
    // 都道府県と海外の選択肢
    const options = [
        "北海道", "青森県", "岩手県", "宮城県", "秋田県",
        "山形県", "福島県", "茨城県", "栃木県", "群馬県",
        "埼玉県", "千葉県", "東京都", "神奈川県", "新潟県",
        "富山県", "石川県", "福井県", "山梨県", "長野県",
        "岐阜県", "静岡県", "愛知県", "三重県", "滋賀県",
        "京都府", "大阪府", "兵庫県", "奈良県", "和歌山県",
        "鳥取県", "島根県", "岡山県", "広島県", "山口県",
        "徳島県", "香川県", "愛媛県", "高知県", "福岡県",
        "佐賀県", "長崎県", "熊本県", "大分県", "宮崎県",
        "鹿児島県", "沖縄県",
        // 海外の主要な国と地域
        "アメリカ合衆国", "カナダ", "イギリス", "フランス", "ドイツ",
        "イタリア", "スペイン", "中国", "韓国", "オーストラリア",
        "ロシア", "ブラジル", "インド", "メキシコ", "南アフリカ",
        // その他の海外の国と地域
        "その他"
    ];

    const locationSelect = document.getElementById("address");

    // 都道府県と海外の選択肢をプルダウンメニューに追加する
    options.forEach(function(option) {
        const optionElement = document.createElement("option");
        optionElement.textContent = option;
        optionElement.value = option;
        locationSelect.appendChild(optionElement);
    });
});


// 性別の選択肢を動的に生成
const genderSelect = document.getElementById('gender');
const genders = ['', '男性', '女性', 'その他'];

genders.forEach(gender => {
    const option = document.createElement('option');
    option.value = gender;
    option.textContent = gender;
    genderSelect.appendChild(option);
});


