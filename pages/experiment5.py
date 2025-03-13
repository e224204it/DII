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
    "穀類":[
        ("ご飯", "中茶碗1杯・もち2個"),
        ("トースト", "6枚切り1枚/2個"),
        
    ],
    "嗜好飲料類":[
        ("緑茶", "120ml"),
        ("紅茶", "150ml"),
        ("ウーロン茶・中国茶", "120ml"),
        ("コーヒー", "150ml"),
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
        # この下から積の和を計算かな？
        total_intake = amout*freq_map[frequency]
        if item in answers_data:
            answers_data[item] += total_intake
        else:
            answers_data[item] = total_intake

# 強化米/麦についての質問
base_options = ["なし・わからない", "あり(複数選択可)"]
rice_options = ["強化米", "麦(七分つき・押し麦)", "胚芽精米", "玄米"]
rice_choice = st.radio("米に強化米や麦などを加えていますか", base_options, horizontal=True, key="rice_choice")
selected_rice = st.multiselect("追加しているものを選択してください", rice_options) if rice_choice == "あり(複数選択可)" else []


# 送信ボタン
st.write("※すべの項目にチェックや数値が入っているかどうか、確認してから送信ボタンを押してください。")
if st.button("送信"):
    tmp_nut_df = pd.DataFrame(answers_data.items(), columns=["食品", "摂取総量"])
    nutrients_columns = nutrients_csv.columns.tolist()[1:38] #謎の38,39が生成される
    for nutrient in nutrients_columns:
        nutrient_dict = nutrients_csv.set_index("食品")[nutrient].to_dict()
        tmp_nut_df[nutrient] = tmp_nut_df["摂取総量"] * tmp_nut_df["食品"].map(nutrient_dict)
    tmp_nut_df = tmp_nut_df.drop(columns="摂取総量")
    st.dataframe(tmp_nut_df) # ここまでで各食品の総栄養素量が求まった
    total_values = tmp_nut_df.drop(columns="食品").sum()
    total_nuts_df = pd.DataFrame([total_values], columns=nutrients_columns[:28])
    # total_nuts_df.insert(0, "トータル", "各総量")
    if "玄米" in selected_rice and "麦(七分つき・押し麦)" in selected_rice:
        brown_rice_nutrients = nutrients_csv[nutrients_csv["食品"] == "玄米"].iloc[:, 1:total_nuts_df.shape[1]]
        barley_nutrients = nutrients_csv[nutrients_csv["食品"] == "麦ご飯"].iloc[:, 1:total_nuts_df.shape[1]]
        # ご飯の摂取量を考慮
        brown_rice_nutrients = brown_rice_nutrients * answers_data.get("ご飯", 0)
        barley_nutrients = barley_nutrients * answers_data.get("ご飯", 0)
        # total_nuts_df に加算（次元を揃える）
        total_nuts_df.iloc[:, 1:] += brown_rice_nutrients.values.flatten() + barley_nutrients.values.flatten()
    elif "麦(七分つき・押し麦)" in selected_rice:
        barley_nutrients = nutrients_csv[nutrients_csv["食品"] == "麦ご飯"].iloc[:, 1:28] * answers_data.get("ご飯", 0)
        total_nuts_df.iloc[0, 1:] += barley_nutrients.values.flatten()
    elif "玄米" in selected_rice:
        brown_rice_nutrients = nutrients_csv[nutrients_csv["食品"] == "玄米"].iloc[:, 1:28] * answers_data.get("ご飯", 0)
        total_nuts_df.iloc[0, 1:] += brown_rice_nutrients.values.flatten()
    st.dataframe(total_nuts_df)
    total_sum = total_nuts_df.select_dtypes(include="number").sum().sum() #これで各栄養素の総量が求まった
    
    # 正規化を行う
    mean_values = dii_param_csv.loc["mean"]
    sd_values = dii_param_csv.loc["S.D"]
    score_values = dii_param_csv.loc["score"]
    total_score = ((norm.cdf(total_sum, mean_values, sd_values)-0.5)*2*score_values).sum()
    st.write(f"あなたのDIIスコアは{total_score}です")