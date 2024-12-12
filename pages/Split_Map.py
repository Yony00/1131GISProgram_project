

import streamlit as st

# 可選項目列表
options = ["男子單打", "男子雙打", "女子單打", "女子雙打", "混合雙打"]

# 預設選中第二項 "男子雙打"
index = 1  # 索引從 0 開始

# 顯示下拉選單
selected_event = st.selectbox(
    "選擇欲查詢的項目",  # 顯示的標題
    options,  # 選項列表
    index=index,  # 預設選中的索引
    key="selectbox_event",  # 唯一的 key
)

# 顯示選中的項目
st.write(f"你選擇了: {selected_event}")
