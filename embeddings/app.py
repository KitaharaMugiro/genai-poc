import openai
import streamlit as st

st.title("LangCore Chatbot")
# APIキーの入力
api_key = st.text_input("Enter your Langcore API Key:", type="password")
# グループ名の入力
group_name = st.text_input("Enter a group name:")

openai.api_base = "https://oai.langcore.org/v1"
openai.api_key = api_key

with st.expander("Click to expand and enter system prompt"):
    system_prompt = st.text_area("Enter system prompt", value="""ユーザの質問に対して、以下の情報を使って答えてください。

{{EMBEDDINGS_CONTEXT}}""")
    
    match_threshold = st.text_input("Embeddings-Match-Threshhold", value="0.5")
    match_count = st.text_input("Embeddings-Match-Count", value="3")


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

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            query=prompt ,
            groupName = group_name,
            headers = {
                "Content-Type": "application/json",
                "LangCore-Embeddings": "on",
                "LangCore-Embeddings-Match-Threshold": match_threshold,
                "LangCore-Embeddings-Match-Count": match_count,
            },
            messages= [
                {
                    "role": "system",
                    "content": system_prompt
                },
                *st.session_state.messages
                ],
                stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "") # type: ignore
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})