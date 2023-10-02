import openai
import streamlit as st

with st.echo(code_location="below"):
    st.title("Azureでの利用方法")

    openai.api_base = "https://oai.langcore.org/v1"
    openai.api_type = "azure"
    openai.api_key = st.secrets["AZURE_OPENAI_API_KEY"]
    openai.api_version = st.secrets["AZURE_OPENAI_API_VERSION"]
    deployment_id = st.secrets["AZURE_DEPLOYMENT_ID"]
    host = st.secrets["AZURE_OPENAI_API_HOST"]

    button = st.button("キャッチコピー生成")
    if button:
        with st.spinner("AIが考え中..."):
            request_body = {
                "deployment_id": deployment_id,
                "headers": {
                    "LangCore-OpenAI-Api-Base": host,
                },
                "messages": [
                    {
                        "role": "system",
                        "content": """#お願い
    あなたは一流の企画担当です。独創的で、まだ誰も思いついていないような、新しいキャッチコピーを1つ出してください。""",
                    },
                    {"role": "user", "content": "最高なキャッチコピーを考えてください。"},
                ],
                "user": "山田太郎",
            }
            response_body = openai.ChatCompletion.create(**request_body)
            result = response_body.choices[0].message.content

            st.subheader("結果:")
            st.write(result)