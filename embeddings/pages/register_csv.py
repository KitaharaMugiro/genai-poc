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

st.title('Langcore Embeddings Register')

# APIキーの入力
api_key = st.text_input("Enter your OpenAI API Key:", type="password")

# グループ名の入力 (オプショナル)
group_name = st.text_input("Enter a group name:")

# csvファイルのアップロード
csv_file = st.file_uploader("Upload a csv file", type="csv")

# ボタンを押したらEmbeddings処理を行う
if st.button("Register Embeddings"):
    if api_key and csv_file:
        lines = csv_file.read().decode('utf-8').split('\n')
        embedded_lines = []

        with st.spinner("Embedding lines..."):
            progress_bar = st.progress(0)
            for index, line in enumerate(lines, 1):
                # Embeddingの処理
                embedded_line = embed_text_with_openai(api_key, line, group_name)
                if embedded_line is not None:
                    embedded_lines.append(embedded_line)

                # 進行度の表示
                progress_bar.progress(index / len(lines))

        st.write("Embeddings completed!")
    else:
        st.warning("Please input API key and text.")
