import streamlit as st

# 設定頁面標題
st.title("清空 st.session_state")

# 測試數據
if "test_data" not in st.session_state:
    st.session_state.test_data = "這是一個測試數據"

# 顯示測試數據
st.write("測試數據:", st.session_state.test_data)

# 設置清空 st.session_state 按鈕
if st.button("清空 st.session_state"):
    st.session_state.clear()
    st.write("st.session_state 已清空")
