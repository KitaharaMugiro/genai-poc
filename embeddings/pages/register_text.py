import streamlit as st
import requests

def embed_text_with_openai(api_key, text, groupName="default"):
    url = "http://langcore.org/api/embeddings"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "input": text,
        "groupName": groupName
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code != 200:
        st.error(f"Error {response.status_code}: {response.text}")
        return None

    return response.json()

st.title('Langcore Embeddings Demo')

# APIキーの入力
api_key = st.text_input("Enter your Langcore API Key:", type="password")

# グループ名の入力 (オプショナル)
group_name = st.text_input("Enter a group name:")

# 複数行のテキストの入力
text_input = st.text_area("Enter multiple lines of text:", height=200)

# ボタンを押したらEmbeddings処理を行う
if st.button("Get Embeddings"):
    if api_key and text_input:
        lines = text_input.split('\n')
        embedded_lines = []

        with st.spinner("Embedding lines..."):
            for index, line in enumerate(lines, 1):
                # Embeddingの処理
                embedded_line = embed_text_with_openai(api_key, line, group_name)
                if embedded_line is not None:
                    embedded_lines.append(embedded_line)

                # 進行度の表示
                st.progress(index / len(lines))

        st.write("Embeddings completed!")
    else:
        st.warning("Please input API key and text.")
