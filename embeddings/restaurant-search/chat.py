import openai
import streamlit as st
import json

# TODO: ログイン機能

# gpt-3.5-turboかgpt4かを選択
is_gpt4 = st.checkbox("Use gpt-4", value=False)

## tuning points ##
system_prompt = """あなたはプロのレストラン検索家です。ユーザの希望に近いお店が「検索結果」に表示されているので、それを元にユーザにおすすめのお店を教えてください。

# 検索ワード
{{EMBEDDINGS_QUERY}}
# 検索結果(ユーザには見えていません)
{{EMBEDDINGS_CONTEXT}}
# 検索結果終わり

上記の情報のみを利用し、確信があることだけ書いてください。
ユーザの希望に合うものが「検索結果」になければ、予算やジャンルなどの条件の見直しをユーザに促してください。
"""
match_threshold = "0.6"
match_count = "5"
functions = [
    {
            "name": "query", 
            "description": "文章からユーザが求めている情報の検索ワードを作成する", 
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "ユーザの会話からユーザの求めているものを検索するためのクエリを作成してください。", 
                    }
                },
                "required": [  "query"], 
            },
        }
    ]
group_name = "foodie"

## tuning points ##


st.title("レストラン検索Chatbot")

openai.api_base = "https://oai.langcore.org/v1"


def function_calling(messages, functions, function_name):
    function_call = "auto"
    if function_name: 
        function_call = {"name": function_name}
    response = openai.ChatCompletion.create(
            model=is_gpt4 and "gpt-4" or "gpt-3.5-turbo",
            messages=messages,
            functions=functions,
            function_call=function_call
    )

    assert "choices" in response, response
    res = response["choices"][0]["message"] # type: ignore
    if "function_call" in res:
        return json.loads(res["function_call"]["arguments"]), True
    return res, False

if "messages" not in st.session_state:
    st.session_state.messages = []

if len(st.session_state.messages) == 0 or st.sidebar.button("Reset chat history"):
    st.session_state.messages.clear()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("銀座のおすすめの寿司を教えて")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # 一旦Function Callingでクエリを考える
        args, is_function_called = function_calling(
            messages=[{"role": "system", "content": system_prompt}, *st.session_state.messages],
            functions=functions,
            function_name="query")

        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model=is_gpt4 and "gpt4" or "gpt-3.5-turbo",
            query=args["query"] ,
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