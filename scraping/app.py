import requests
from xml.etree import ElementTree
import streamlit as st
from trafilatura import fetch_url, extract
from trafilatura.settings import use_config


def main():
    st.title("パレオスクレイピング")
    st.write("まずブログポストのURLの一覧を取得します")

    if st.button("一覧取得"):
        sitemap_index = "https://yuchrszk.blogspot.com/sitemap.xml"
        urls = fetch_sitemap_urls(sitemap_index)
        # data = save_urls_to_file(urls, "sitemap_urls.txt")

        st.download_button(
            "ダウンロードする", urls_to_string(urls), file_name="sitemap_urls.txt"
        )

        if urls:
            st.write("最初の10件のテキストを取得して表示します。")
            contents = []
            for url in urls[:10]:
                content = fetch_contents(url)
                contents.append({"url": url, "content": content})

            st.json(contents)


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


def save_urls_to_file(urls: list, filename: str) -> None:
    """URLのリストを指定したファイルに保存する関数"""
    with open(filename, "w") as file:
        for url in urls:
            file.write(url + "\n")


if __name__ == "__main__":
    main()
