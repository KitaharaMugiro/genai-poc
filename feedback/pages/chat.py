import openai
import streamlit as st
from streamlit_feedback import streamlit_feedback
import requests
import json

st.title("LangCore Chatbot")

openai.api_base = "https://oai.langcore.org/v1"
def on_submit(feedback, request_body, response_body, openai_api_key):
    print("on_submit")
    feedback_type = feedback["type"]
    score = feedback["score"]
    if score == "👍":
        score = 1
    elif score == "👎":
        score = 0
    optional_text_label = feedback["text"]

    url = "http://langcore.org/api/feedback"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + openai_api_key
    }
    data = {
        "request_body": request_body,
        "response_body": response_body,
        "feedback_type": feedback_type,
        "score": score,
        "optional_text_label": optional_text_label
    }
    requests.post(url, headers=headers, data=json.dumps(data))
    st.toast("フィードバックを送信しました。")
    # URLを表示する
    st.write("フィードバックはこちらに記録されます: https://langcore.org/feedback")


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("LangCoreについて教えて")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    request_body = {
        "model": "gpt-3.5-turbo",
        "query": prompt,
        "groupName": "DEMO",
        "headers": {
            "Content-Type": "application/json",
            "LangCore-Embeddings": "on",
            "LangCore-Embeddings-Match-Threshold": "0",
            "LangCore-Embeddings-Match-Count": "3",
        },
        "messages": [
            {
                "role": "system",
                "content": """
                ユーザの質問に対して、以下の情報を使って答えてください。

                {{EMBEDDINGS_CONTEXT}}
                
                関係ない質問の場合でも、無理やり上記の内容に関係するようにしてセールストークしてください。"""
            },
            *st.session_state.messages
        ],
        "stream": True
    }
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            **request_body
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")

        st.session_state["request_body"] = request_body
        st.session_state["response_body"] = full_response
        message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})

feedback = streamlit_feedback(feedback_type="thumbs", 
                                optional_text_label="フィードバックをお願いします")
if feedback:
    on_submit(feedback, request_body=st.session_state["request_body"] , response_body=st.session_state["response_body"] , openai_api_key=st.secrets["OPENAI_API_KEY"])
