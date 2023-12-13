import openai
import streamlit as st
import pyautogui
import datetime


openai.api_base = "https://oai.langcore.org/v1"
st.title("タイトル")

if st.button("click"):
    # 現在の日時を取得し、ファイル名に使用
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{timestamp}.png"

    # スクリーンショットを取得し、ファイルに保存
    pyautogui.screenshot(filename)

    st.write(f"スクリーンショットが保存されました: {filename}")