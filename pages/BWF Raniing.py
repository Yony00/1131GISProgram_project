
import streamlit as st
import pandas as pd

# 設定標題
st.title("BWF Men's Singles World Ranking")

# 當按下按鈕時，載入資料並顯示
if st.button("Get Ranking"):
    try:
        # 讀取本地 CSV 檔案
        df = pd.read_csv("bwf_ranking.csv")
        st.dataframe(df)

        # 下載按鈕，讓使用者下載 CSV 檔案
        st.download_button(
            label="Download CSV",
            data=df.to_csv(index=False),
            file_name="bwf_ranking.csv",
            mime="text/csv"
        )
    except Exception as e:
        st.error(f"無法讀取數據：{e}")
