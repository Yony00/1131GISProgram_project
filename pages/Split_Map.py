import streamlit as st
import leafmap.foliumap as leafmap

options = list(("男子單打","男子雙打","女子單打","女子雙打","混合單打"))
index = options[1]

selected_date1 = st.selectbox(
    "選擇欲查詢的日期 (預設最新日期)",
    options,
    index=index,
    key="selectbox_date1",  # 添加唯一的 key
)
