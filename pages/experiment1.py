import streamlit as st
import pandas as pd
import io
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_dir, "../data", "foods_data.csv")
nutrients_csv = pd.read_csv(csv_path)

st.title("食品摂取アンケート")
st.write("※記入上の注意をよく読んで回答してください")

# カテゴリごとのデータ（目安量を追加）
foods = {
    "卵":[
        ("卵", "1個分"),
    ],
    "乳類":[
        ("牛乳", "180ml"),
        ("ヨーグルト", "小1カップ/コップ半杯"),
        ("チーズ", "1個・1枚"),
        ("乳製品", "中1皿分"),
    ],
    "肉類":[
        ("肉(かたまり)主体料理", "中1皿"),
        ("肉煮込み料理", "中1皿"),
        ("肉炒め", "中1皿・中1杯分"),
        ("ハム・ベーコン・焼き豚・ソーセージ", "2枚・2本"),
        ("レバー・もつ", "1串・小1皿分"),
    ],
    "魚介類":[
        ("生魚", "中1皿"),
        ("加熱した魚", "中1切"),
        ("タコ・イカ・エビ・カニ・貝類", "小鉢1杯分"),
        ("かまぼこ・さつま揚げ・竹輪", "小1皿分"),
        ("小魚", "小さじ1杯分"),
        ("魚介・魚卵塩蔵品", "小1皿分"),
    ],
    "豆類":[
        ("豆腐・厚揚げ・がんも", "1/4丁・中1皿分"),
        ("油揚げ", "寿司あげ1枚分"),
        ("納豆・豆", "小1皿分"),
        ("味噌", "汁椀1敗・小鉢1杯"),
    ],
    "緑黄色野菜":[
        ("ほうれん草・にら・青菜類", "小皿・小鉢1杯分"),
        ("トマト・ブロッコリー", "小皿・小鉢1杯分"),
        ("かぼちゃ", "小皿・小鉢1杯分"),
        ("人参・ピーマン・サヤインゲンなど", "小皿・小鉢1杯分"),
        ("薬味野菜", "小さじ山盛り1杯分"),
    ],
    "淡色野菜":[
        ("玉ねぎ・根深ねぎ", "中1皿・中1杯分"),
        ("大根・かぶ・れんこん・ごぼう", "小皿・小鉢1杯分"),
        ("きゅうり・なす", "小皿・小鉢1杯分"),
        ("キャベツ・レタス・白菜・もやしなど", "小皿・小鉢1杯分"),
    ],
    "果物":[
        ("果物", "みかん：中1個, りんご・なし・柿：1/2個, バナナ1本・いちご：中5個"),
    ],
    "茸":[
        ("しいたけ・しめじ・えのき", "小1皿分"),
    ],
    "海藻":[
        ("わかめ・のり・昆布・ひじき", "汁椀1杯分/1個分"),
        ("ところてん・寒天", "小鉢1杯分"),
    ],
    "芋類":[
        ("こんにゃく", "小鉢1杯分"),
        ("じゃが芋・里芋・山芋", "中1皿・中1杯分"),
        ("さつまいも", "1/3個・1杯分"),
    ],
    "穀類":[
        ("白米", "中茶碗1杯・もち2個"),
        ("トースト", "6枚切り1枚/2個"),
        ("マーガリン", "トースト1枚分"),
        ("バター", "トースト1枚分"),
        ("菓子パン・調理パン", "1個"),
        ("和麺", "丼ぶり1杯"),
        ("中華麺", "中1杯"),
        ("パスタ", "中1皿分"),
    ],
    "バランス栄養補助食品":[
        ("補助食品", "1回に約200kcal"),
    ],
    "菓子類":[
        ("甘くない菓子", "片手1杯分"),
        ("甘い和菓子", "1個/2-3個"),
        ("乳製品を使った洋菓子", "1個"),
        ("その他の甘い洋菓子", "1個/4-5枚/3個"),
        ("ジャム・はちみつ", "小さじ2杯分"),
    ],
    "油脂類":[
        ("揚げ物", "中1皿分"),
        ("炒め物", "中1皿分"),
        ("マヨネーズ・ドレッシング", "中1皿分"),
    ],
    "種実類":[
        ("ごま", "小さじ1杯分"),
        ("ナッツ類", "小1皿分"),
    ],
    "嗜好飲料類":[
        ("緑茶", "120ml"),
        ("ウーロン茶・中国茶", "120ml"),
        ("紅茶", "150ml"),
        ("コーヒー", "150ml"),
        ("コーヒー・紅茶に入れる砂糖", "小さじ1杯"),
        ("その他の茶", "120ml"),
        ("野菜　100%ジュース", "180ml"),
        ("果汁　100%ジュース", "180ml"),
        ("甘い飲料", "180ml"),
        ("スポーツ飲料", "180ml"),
    ],
    "塩類":[
        ("汁物", "汁椀1杯"),
        ("煮物", "中1皿"),
        ("漬物", "小1皿"),
    ],
    "酒":[
        ("日本酒", "180cc"),
        ("焼酎", "180cc"),
        ("果実酒・酎ハイ", "180cc"),
        ("ビール(ビン大)", "ビン大"),
        ("ビール(ビン中)", "ビン中"),
        ("ビール(ビン小)", "ビン小"),
        ("ビール(カン大)", "カン大"),
        ("ビール(カン中)", "カン中"),
        ("ビール(カン小)", "カン小"),
        ("ビール(ジョッキ・グラス大)", "ジョッキ・グラス大"),
        ("ビール(ジョッキ・グラス中)", "ジョッキ・グラス中"),
        ("ビール(ジョッキ・グラス小)", "ジョッキ・グラス小"),
        ("ウイスキー", "30cc"),
        ("ワイン・カクテル", "100cc"),
    ]
}

# 摂取頻度の選択肢
frequency_options = ["毎日", "週5-6", "週2-4", "週1", "月1-3", "無"]

# 月あたり摂取頻度の数値化
freq_map = {"毎日": 1, "週5-6": 5.5/7, "週2-4": 3/7, "週1": 1/7, "月1-3": 1/15, "無": 0}

# 回答データを格納するリスト
answers_data = {}

# 各食品ごとに入力フォームを作成
for category, items in foods.items():
    st.subheader(category)
    for item, portion in items:
        frequency = st.radio(f"**{item}**　目安量＝{portion}", frequency_options, horizontal=True, key=item)
        amount = st.number_input("摂取量(数値)", min_value=0.01, value=1.0, step=1.0, key=f"amount_{item}") if frequency != "無" else 0
        total_intake = freq_map[frequency] * amount #摂取総量の計算
        if item in answers_data:
            answers_data[item] += total_intake
        else:
            answers_data[item] = total_intake

# 送信ボタン
st.write("※すべの項目にチェックや数値が入っているかどうか、確認してから送信ボタンを押してください。")
if st.button("送信"):
    df = pd.DataFrame(answers_data.items(), columns=["食品", "摂取総量"])
    nutrients_columns = nutrients_csv.columns.tolist()[1:]
    for nutrient in nutrients_columns:
        nutrients_dict = nutrients_csv.set_index("食品")[nutrient].to_dict()
        df[nutrient] = df["摂取総量"] * df["食品"].map(nutrients_dict)
    df = df.drop(columns="摂取総量")
    st.success("アンケートが終了しました！")
    st.dataframe(df)

    # shift-jisのcsvを保存
    csv_buffer_jis = io.BytesIO()
    df.to_csv(csv_buffer_jis, index=False, encoding="shift-jis")
    csv_data_jis = csv_buffer_jis.getvalue()
    st.download_button(
        label="survey_results_shift-jis.csvをダウンロード(Excel向け)",
        data=csv_data_jis,
        file_name="survey_results_shift-jis.csv",
        mime="text/csv",
    )