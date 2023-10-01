import streamlit as st
import requests


def embed_text_with_openai(api_key, text, metadata_input, groupName="default"):
    url = "http://langcore.org/api/embeddings"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {"input": text, "groupName": groupName, "metadata": metadata_input}

    response = requests.post(url, json=data, headers=headers)

    if response.status_code != 200:
        st.error(f"Error {response.status_code}: {response.text}")
        return None

    return response.json()


st.title("Langcore テキスト登録画面(メタデータ付き)")
st.text("メタデータ付きでベクトルDBに追加します")

# APIキーの入力
api_key = st.text_input("Enter your OpenAI API Key:", type="password")

# グループ名の入力 (オプショナル)
group_name = st.text_input("Enter a group name:")

# 複数行のテキストの入力
text_input = st.text_input("Enter a text")
metadata_input = st.text_input("Enter metadata")


def split_string_into_chunks(text):
    return text.split("\n")


# ボタンを押したらEmbeddings処理を行う
if st.button("Register Embeddings"):
    if api_key and text_input and metadata_input:
        with st.spinner("Embedding..."):
            embed_text_with_openai(api_key, text_input, metadata_input, group_name)

        st.write("Embeddings completed!")
    else:
        st.warning("Please input API key and text.")
