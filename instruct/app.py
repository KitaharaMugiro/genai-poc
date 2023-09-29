import openai
import streamlit as st

# この行を追加することでLangCoreでログを残すことができます
openai.api_base = "https://oai.langcore.org/v1"

def main():
    st.title("ChatGPT キャッチコピー作成アプリ")
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
