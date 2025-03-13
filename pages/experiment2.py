import streamlit as st
import pandas as pd
import io
import os
from scipy.stats import norm

current_dir = os.path.dirname(os.path.abspath(__file__))
foods_data_path = os.path.join(current_dir, "../data", "foods_data.csv")
dii_param_path = os.path.join(current_dir, "../data", "dii_param2.csv")
nutrients_csv = pd.read_csv(foods_data_path)
dii_param_csv = pd.read_csv(dii_param_path)

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
    nutrients_columns = nutrients_csv.columns.tolist()[1:38] #謎の38,39が生成される
    for nutrient in nutrients_columns:
        nutrients_dict = nutrients_csv.set_index("食品")[nutrient].to_dict()
        df[nutrient] = df["摂取総量"] * df["食品"].map(nutrients_dict) #総栄養素量が求まる
    df = df.drop(columns="摂取総量")
    # ここから下に書く
    dii_param_columns = dii_param_csv.columns.tolist()[1:]
    for param in dii_param_columns:
        # dfにdiiのカラムを追加する
        dii_param_dict = dii_param_csv.set_index("パラメータ")[param].to_dict()
        df[param] = df[(norm.cdf(1441.992262, 2056, 338)-0.5)*2*0.18] #norm.cdfをmapなどを使えば組み込めそう？
        # df[param] = df[] #norm.cdfをmapなどを使えば組み込めそう？
    st.success("アンケートが終了しました！")
    st.dataframe(df)
