import openai
import streamlit as st

openai.api_base = "https://oai.langcore.org/v1"



def summarize(url):
    from trafilatura import fetch_url, extract
    from trafilatura.settings import use_config
    config = use_config()
    config.set("DEFAULT", "EXTRACTION_TIMEOUT", "0")
    config.set("DEFAULT", "MIN_EXTRACTED_SIZE", "100")
    downloaded = fetch_url(url)
    result = extract(downloaded, config=config)

    # テキストが長すぎる場合は、一部を削除します。
    content = result
    if len(content) > 1000: 
        content = result[:1000]
    
    prompt = f"""貴方は文章分析の専門家として提供されたウェブページの内容を人にわかりやすく伝わるように100文字程度で簡潔に要約してください。
ウェブページの内容は ``` で括って提供されます。
ウェブページの本文が長い場合は途中で切られて提供されます。
ウェブページの内容の HTML 要素から何を強調するか考えてください。
出力は日本語のマークダウン形式でお願いします。

ウェブページ
```
{content}
```

では、日本語でよろしくお願いします
    """

    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": prompt
            },
        ]

    )
    summarized_text = res.choices[0].message.content # type: ignore

    return  summarized_text , prompt


def main():
    st.title('URL先の文章を要約するツール')
    st.write('URLを入力すると、その内容を元にChatGPTを使ってメールを自動作成するツールです。')

    url = st.text_input('URL', "https://qiita.com/yuno_miyako/items/ce80002adf76bd321ad3")
    if st.button('要約する'):
        with st.spinner('要約作成中...'):
            summarized_text, prompt = summarize(url)
        st.text_area("作成された要約", summarized_text, height=300)

        expander = st.expander("実行したプロンプト", expanded=False)
        with expander:
            st.text(prompt)

    
if __name__ == '__main__':
    main()
