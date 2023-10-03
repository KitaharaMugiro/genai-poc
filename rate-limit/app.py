import openai
import streamlit as st

openai.api_base = "https://oai.langcore.org/v1"


def main():
    st.title("利用回数制限のデモ")
    st.text("LangCore SaaSの利用回数制限を確認するためのデモです。")
    st.text("今回は1分間あたり1回までの利用制限を加えています。")
    user_input = st.text_input("キャッチコピーを作成するためのキーワードを入力してください: ")
    if st.button("キャッチコピーを生成"):
        catchphrase = call_chatgpt_api(user_input)
        st.write("生成されたキャッチコピー: ", catchphrase)


def call_chatgpt_api(input_text):
    try:
        prompt = f"""次のお題からキャッチコピーを作成してください。
お題: {input_text}
"""
        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            temperature=0.7,
            max_tokens=100,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"エラー: キャッチコピーを生成できませんでした。{str(e)}"


if __name__ == "__main__":
    main()
