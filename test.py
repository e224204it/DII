from scipy.stats import norm
import streamlit as st
import pandas as pd
import io
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
# foods_data_path = os.path.join(current_dir, "/data", "foods_data.csv")
dii_param_path = os.path.join(current_dir, "data", "dii_param2.csv")
# nutrients_csv = pd.read_csv(foods_data_path)
dii_param_csv = pd.read_csv(dii_param_path)


# 累積分布関数を使いながら正規化
print((norm.cdf(1441.992262, 2056, 338)-0.5)*2*0.18)

import pandas as pd

# DataFrame の作成（dii_param_csvが辞書型のデータである場合）
df = pd.DataFrame(dii_param_csv)

# 1列目（食品名）を除いたカラムをループ
for i in range(len(df.columns)):
    column_name = df.columns[i]  # カラム名を取得
    for index, value in df[column_name].items():  # 各行の値を取得
        print((norm.cdf(value, mean, SD)-0.5)*2*score)  # 食品名と値を表示


