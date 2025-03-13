import streamlit as st
import pandas as pd
import io
import os
from scipy.stats import norm

current_dir = os.path.dirname(os.path.abspath(__file__))
foods_data_path = os.path.join(current_dir, "../data", "foods_data.csv")
dii_param_path = os.path.join(current_dir, "../data", "dii_param.csv")
nutrients_csv = pd.read_csv(foods_data_path)
dii_param_csv = pd.read_csv(dii_param_path, index_col=0)

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

frequecy_options = ["毎日", "週5-6", "週2-4", "週1", "月1-3", "無"]
freq_map = {"毎日": 1, "週5-6": 5.5/7, "週2-4": 3/7, "週1": 1/7, "月1-3": 1/15, "無": 0}
answers_data = {}

for category, items in foods.items():
    st.subheader(category)
    for item, portion in items:
        frequency = st.radio(f"**{item}**　目安量＝{portion}", frequecy_options, horizontal=True, key=item)
        # 最後のif文必要か？
        amout = st.number_input("摂取量(数値)", min_value=0.01, value=1.0, step=1.0, key=f"amout_{item}") if frequency != "無" else 0
        total_intake = freq_map[frequency]*amout
        if item in answers_data:
            answers_data[item] += total_intake
        else:
            answers_data[item] = total_intake

# 送信ボタン
st.write("※すべの項目にチェックや数値が入っているかどうか、確認してから送信ボタンを押してください。")
if st.button("送信"):
    tmp_nut_df = pd.DataFrame(answers_data.items(), columns=["食品", "摂取総量"])
    nutrients_columns = nutrients_csv.columns.tolist()[1:38] #謎の38,39が生成される
    for nutrient in nutrients_columns:
        nutrient_dict = nutrients_csv.set_index("食品")[nutrient].to_dict()
        tmp_nut_df[nutrient] = tmp_nut_df["摂取総量"] * tmp_nut_df["食品"].map(nutrient_dict)
    tmp_nut_df = tmp_nut_df.drop(columns="摂取総量")
    st.dataframe(tmp_nut_df)
    # ここまでで食品の総栄養素量が求まった
    total_values = tmp_nut_df.drop(columns="食品").sum()
    total_nuts_df = pd.DataFrame([total_values], columns=nutrients_columns[:28])
    total_nuts_df.insert(0, "トータル", "各総量")
    st.dataframe(total_nuts_df)
    total_sum = total_nuts_df.select_dtypes(include="number").sum().sum() #これで各栄養素の総量が求まった
    # st.write(total_sum)
    
    # 正規化を行う
    mean_values = dii_param_csv.loc["mean"]
    sd_values = dii_param_csv.loc["S.D"]
    score_values = dii_param_csv.loc["score"]
    
    # final_score = (norm.cdf(total_sum, mean, sd)-0.5)*2*score
    # st.write(f"あなたのDIIスコアは{final_score}です")
    
    # st.write(total_values)
    total_score = ((norm.cdf(total_sum, mean_values, sd_values)-0.5)*2*score_values).sum()
    st.write(f"あなたのDIIスコアは{total_score}です")