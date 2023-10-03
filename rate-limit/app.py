import streamlit as st

with st.echo(code_location="below"):
    import openai
    import streamlit as st

    openai.api_base = "https://oai.langcore.org/v1"

    st.title("利用回数制限のデモ")
    st.text("LangCore SaaSの利用回数制限を確認するためのデモです。")
    st.text("今回は1分間あたり1回までの利用制限を加えています。")
    user_input = st.text_input("キャッチコピーを作成するためのキーワードを入力してください: ", "夏の思い出")
    if st.button("キャッチコピーを生成"):
        try:
            prompt = f"次のお題からキャッチコピーを作成してください。お題: {user_input}"
            response = openai.Completion.create(
                model="gpt-3.5-turbo-instruct",
                prompt=prompt,
                temperature=0.7,
                max_tokens=100,
            )
            st.write("生成されたキャッチコピー: " + response.choices[0].text.strip())
        except Exception as e:
            st.error("エラーが発生しました。 " + str(e))
