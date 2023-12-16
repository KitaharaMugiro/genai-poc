import streamlit as st
import requests


def embed_text_with_azure(api_key, text, azure_resource_name,azure_deployment_name, groupName="default"):
    url = "http://langcore.org/api/embeddings"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {"input": text, "groupName": groupName, 
            "azure_resource_name": azure_resource_name,
            "azure_deployment_name": azure_deployment_name
            }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code != 200:
        st.error(f"Error {response.status_code}: {response.text}")
        return None

    return response.json()


st.title("Langcore Azure テキスト登録画面")
st.text("１行ずつをチャンクとしてベクトルDBに追加します")

# APIキーの入力
api_key = st.text_input("Enter your OpenAI API Key:", type="password")

# グループ名の入力 (オプショナル)
group_name = st.text_input("Enter a group name:")

# 複数行のテキストの入力
text_input = st.text_area("Enter multiple lines of text:", height=200)

resource_name = st.text_input("Enter your Azure resource name:")
deployment_name = st.text_input("Enter your Azure deployment name:")

def split_string_into_chunks(text):
    return text.split("\n")


# ボタンを押したらEmbeddings処理を行う
if st.button("Register Embeddings"):
    if api_key and text_input:
        lines = []
        # 100文字の塊を作る
        lines = split_string_into_chunks(text_input)

        with st.spinner("Embedding lines..."):
            progress_bar = st.progress(0)
            for index, line in enumerate(lines, 1):
                # Embeddingの処理
                embed_text_with_azure(api_key, line, resource_name, deployment_name, group_name)
                # 進行度の表示
                progress_bar.progress(index / len(lines))

        st.write("Embeddings completed!")
    else:
        st.warning("Please input API key and text.")
