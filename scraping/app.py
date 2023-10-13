import requests
from xml.etree import ElementTree
import streamlit as st
from trafilatura import fetch_url, extract
from trafilatura.settings import use_config
import openai


def main():
    st.title("パレオスクレイピング")
    st.write("まずブログポストのURLの一覧を取得します")

    start_number = st.number_input("開始番号", value=0)
    count_number = st.number_input("取得件数", value=100)

    if st.button("一覧取得"):
        sitemap_index = "https://yuchrszk.blogspot.com/sitemap.xml"
        urls = fetch_sitemap_urls(sitemap_index)

        if urls:
            st.write(f"{start_number}からのポストを{count_number}件のテキストを取得して表示します。")
            contents = []
            for url in urls[start_number : start_number + count_number]:
                content = fetch_contents(url)
                summarized_content = summarize(content)
                contents.append(
                    {"url": url, "content": summarized_content, "is_summarized": True}
                )
                embed_text_with_openai(
                    st.secrets["OPENAI_API_KEY"],
                    summarized_content,
                    url,
                    groupName="parao",
                )


def embed_text_with_openai(api_key, text, metadata_input, groupName="default"):
    url = "http://langcore.org/api/embeddings"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {"input": text, "groupName": groupName, "metadata": metadata_input}

    response = requests.post(url, json=data, headers=headers)

    if response.status_code != 200:
        st.error(f"Error {response.status_code}: {response.text}")
        return None

    return response.json()


def summarize(content: str) -> str:
    content = content[:3000]
    prompt = f"""貴方は文章分析の専門家として提供されたウェブページの内容を人にわかりやすく伝わるように100文字程度で簡潔に要約してください。
ウェブページの内容は ``` で括って提供されます。
重要なポイントを抑えて要約してください。
ウェブページの本文が長い場合は途中で切られて提供されます。
出力は日本語でお願いします。

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
            {"role": "system", "content": prompt},
        ],
    )
    summarized_text = res.choices[0].message.content  # type: ignore
    return summarized_text


def fetch_contents(url: str) -> str:
    config = use_config()
    config.set("DEFAULT", "EXTRACTION_TIMEOUT", "0")
    config.set("DEFAULT", "MIN_EXTRACTED_SIZE", "100")
    downloaded = fetch_url(url)
    result = extract(downloaded, config=config)
    return result


def urls_to_string(urls: list) -> str:
    """URLのリストを文字列に変換する関数"""
    return "\n".join(urls)


def fetch_sitemap_urls(sitemap_url: str) -> list:
    """指定したサイトマップまたはサイトマップインデックスURLからURLのリストを取得する関数"""
    response = requests.get(sitemap_url)
    xml_content = response.content

    root = ElementTree.fromstring(xml_content)
    namespaces = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}

    # サイトマップURLを取得
    sitemap_urls = [loc.text for loc in root.findall("sm:sitemap/sm:loc", namespaces)]

    # URLエントリを取得 (サイトマップ内のURL)
    entry_urls = [loc.text for loc in root.findall("sm:url/sm:loc", namespaces)]

    # サイトマップURLが存在する場合、再帰的にURLを取得
    for s_url in sitemap_urls:
        entry_urls.extend(fetch_sitemap_urls(s_url))

    return entry_urls


if __name__ == "__main__":
    ## login ##
    password = st.text_input("Password", type="password")
    if password == "":
        pass
    elif password != st.secrets["PASSWORD"]:
        st.error("the password you entered is incorrect")
        st.stop()
    else:
        main()
