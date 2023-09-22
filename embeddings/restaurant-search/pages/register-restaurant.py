import streamlit as st
import requests
import pandas as pd

## tuning points ##
group_name = "foodie"
api_key = st.secrets["OPENAI_API_KEY"]

## tuning points ##

def embed_text_with_openai(text, metadata_input):
    url = "http://langcore.org/api/embeddings"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "input": text,
        "groupName": group_name,
        "metadata": metadata_input
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code != 200:
        st.error(f"Error {response.status_code}: {response.text}")
        return None

    return response.json()

st.title('お店登録')


# 複数行のテキストの入力
store_name = st.text_input("店名")
area_name = st.text_input("エリア")
genre_name = st.text_input("ジャンル")
budget = st.text_input("予算")
features = st.text_input("お店の特徴")
menu = st.text_input("看板メニュー")
internet_reservation = st.text_input("ネット予約")
private_room = st.text_input("個室")
reservation_difficulty = st.text_input("予約困難度")
url = st.text_input("食べログURL")
map_url = st.text_input("マップURL")

text_input = f"""
店名: {store_name}
エリア: {area_name}
ジャンル: {genre_name}
予算: {budget}
お店の特徴: {features}
看板メニュー: {menu}
ネット予約: {internet_reservation}
個室: {private_room}
予約困難度: {reservation_difficulty}
"""

metadata_input = f"""
食べログURL: {url}
マップURL: {map_url}
"""

# ボタンを押したらEmbeddings処理を行う
if st.button("Register Embeddings"):
    if text_input and metadata_input:
        with st.spinner("Embedding..."):
            embed_text_with_openai(text_input, metadata_input )
        st.write("登録完了!")
    else:
        st.warning("Please enter text and metadata")



# excelをアップロードして一括登録

def format_data(record):
    store_name = record['店名']
    area_name = record['エリア']
    genre_name = record['ジャンル']
    budget = record['予算']
    features = record['お店の特徴']
    menu = record['看板メニュー']
    internet_reservation = record['ネット予約可否']
    private_room = record['個室有無']
    reservation_difficulty = record['予約困難度']
    url = record['URL(食べログ)']
    map_url = record['地図']
    
    text_input = f"""
店名: {store_name}
エリア: {area_name}
ジャンル: {genre_name}
予算: {budget}
お店の特徴: {features}
看板メニュー: {menu}
ネット予約: {internet_reservation}
個室: {private_room}
予約困難度: {reservation_difficulty}
"""
    
    metadata_input = f"""
食べログURL: {url}
マップURL: {map_url}
"""
    
    return text_input, metadata_input


uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    data = pd.read_excel(uploaded_file)
    data.columns = data.iloc[0]
    data = data.drop(0)
    
    with st.spinner("Embedding lines..."):
        for index, row in data.iterrows():
            text_input, metadata_input = format_data(row)
            embed_text_with_openai(text_input, metadata_input )
    st.write("Embeddings completed!")