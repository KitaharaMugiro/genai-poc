# URLから自動で情報を取得して登録する

import uuid
from bs4 import BeautifulSoup
import requests
import streamlit as st
import openai
from trafilatura import fetch_url, extract
from trafilatura.settings import use_config
from supabase import create_client, Client
import json

# パスワード入力画面
password = st.text_input("パスワード", type="password")
if password != st.secrets["PASSWORD"]:
    st.error("パスワードが違います。")
    st.stop()
openai.api_type = "openai"
SUPABASE_URL = st.secrets['NEXT_PUBLIC_SUPABASE_URL']
SUPABASE_KEY = st.secrets['SUPABASE_SECRET_KEY']
if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("Missing SUPABASE_URL or SUPABASE_KEY environment variable.")
    st.stop()

# Create a client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# タグの一覧を取得
def list_tags():
    res = supabase.table("tags").select("*").execute()
    data = res.data
    return data

def list_price_types():
    res = supabase.table("price_type").select("*").execute()
    data = res.data
    return data

def get_parameters(homepage_url, tags, price_types):
    config = use_config()
    config.set("DEFAULT", "EXTRACTION_TIMEOUT", "0")
    config.set("DEFAULT", "MIN_EXTRACTED_SIZE", "1000")
    downloaded = fetch_url(homepage_url)
    result = extract(downloaded, config=config)
    # TODO: ここで取得しているテキストがイマイチな可能性が高い
    # テキストが長すぎる場合は、一部を削除します。
    content = result
    if content is None or len(content) == 0:
        raise Exception("ホームページから情報を取得できませんでした。")
    # if len(content) > 2000:
    #     content = result[:2000]

    tags_str = ", ".join(tags)
    price_types_str = ", ".join(price_types)

    prompt = f"""
    ホームページ情報 {{
    {content}
    }}"""  + """

    上記の情報から以下の形式でJSONを作成してください。
    {
        "name": "ツールの名前",
        "description": "ツールの説明文",
        "price_type": enum($PRICE_TYPES_LIST),
        "price": text (ex: 3,900円/月〜, 20ドル/月〜), ),
        "is_japanese_tool": boolean,
        "is_login": boolean,
        "tags" : list of up to 3 [$TAGS_LIST],
    }

    descriptionの制約条件
    - ホームページ情報を見て、このツールの日本語の説明文を作成してください。
    - ツールの名前やAIについては書かなくても大丈夫です。
    - 読み手は、このツールを使って何ができるのかを知りたいと思っています。他の情報は含めないでください。
    - 「」や""などで全体を囲わないでください。
    - 100文字以内でわかりやすく簡潔に、何に役に立つのかを書いてください。
    """

    prompt = prompt.replace("$TAGS_LIST", tags_str)
    prompt = prompt.replace("$PRICE_TYPES_LIST", price_types_str)

    request_body = {
        "model": "gpt-4o",
        "messages": [
            {"role": "system", "content": prompt},
        ],
        "response_format":{"type": "json_object"},
        "user": "ai-tool-navi",
    }
    res = openai.chat.completions.create(**request_body)
    description = res.choices[0].message.content
    return description

def get_ogp_image(homepage_url):
    # ウェブページのHTMLを取得
    response = requests.get(homepage_url)
    if response.status_code != 200:
        return None

    # HTMLを解析
    soup = BeautifulSoup(response.text, 'html.parser')

    # OGP画像のURLを探す
    og_image = soup.find('meta', property='og:image')
    if og_image and og_image.get('content'):
        return og_image['content']
    return None

def app():
    # Fetch data from supabase
    url = st.text_input("URL")
    tags_objects = list_tags()
    price_types_objects = list_price_types()

    price_types = [d.get("name") for d in price_types_objects]
    tags =   [d.get("name") for d in tags_objects]

    # homepage_urlを取得
    if st.button("データ取得"):
        parameters = get_parameters(url, tags, price_types)
        ogp_image_url = get_ogp_image(url)
        
        # 画像を取得して、supabaseに保存する
        public_url = ""
        if ogp_image_url:
            response = requests.get(ogp_image_url)
            if response.status_code == 200:
                uuid_str = str(uuid.uuid4())
                path = f"auto-register/{uuid_str}"
                supabase.storage.from_("tools").upload(path, response.content, file_options={"content-type": "image/webp"})

                public_url = supabase.storage.from_("tools").get_public_url(path)
                ogp_image_url = public_url
            else:
                public_url = ""
        
        st.json(parameters)
        if public_url: 
            st.image(public_url)
        else :
            st.warning("OGP画像が取得できませんでした。")

        parameters = json.loads(parameters)

        # paramters["price_type"]をprice_type_idに変換する
        price_type_id = None
        for price_type in price_types_objects:
            if price_type.get("name") == parameters.get("price_type"):
                price_type_id = price_type.get("id")
                break
        
        # paramters["tags"]をtag_idsに変換する
        tag_ids = []
        for tag in tags_objects:
            if tag.get("name") in parameters.get("tags"):
                tag_ids.append(tag.get("id"))

        res = supabase.table("tools").insert([{
            "name": parameters.get("name"),
            "description": parameters.get("description"),
            "description_ai": parameters.get("description"),
            "description_old": parameters.get("description"),
            "image_url": ogp_image_url,
            "homepage_url": url,
            "price_type_id": price_type_id,
            "price": parameters.get("price"),
            "is_japanese_tool": parameters.get("is_japanese_tool"),
            "is_login": parameters.get("is_login"),
            "updated_at": "now()",
        }]).execute()

        # tool_idを取得する
        tool_id = res.data[0].get("id")

        
        # tools_tagsに登録する
        for tag_id in tag_ids:
            supabase.table("tools_tags").insert([{
                "tool_id": tool_id,
                "tag_id": tag_id,
            }]).execute()

        url = f"https://www.ai-navi.news/admin/tools/{tool_id}/edit"
        st.success("登録が完了しました。")
        st.markdown(f"[登録したツールを編集する]({url})")
        






if __name__ == "__main__":
    app()
