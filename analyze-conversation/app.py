import streamlit as st
import json

# ファイルアップロード機能の作成
uploaded_file = st.file_uploader("JSONファイルをアップロードしてください", type="json")

if uploaded_file:
    # アップロードされたJSONファイルの読み込み
    data = json.load(uploaded_file)

    # 検索バーの作成
    query = st.text_input("検索キーワードを入力してください:")

    if query:
        results = []

        for entry in data:
            for key, value in entry["mapping"].items():
                if "message" in value and value["message"]:
                    content = value["message"].get("content", {})
                    # 'parts'キーが存在するか確認
                    if "parts" in content:
                        for part in content["parts"]:
                            if query in part:
                                results.append(part)

        # 検索結果の表示
        if results:
            st.write(f"'{query}'に関連するメッセージ:")
            for result in results:
                st.write(result)
        else:
            st.write(f"'{query}'に関連するメッセージは見つかりませんでした。")

else:
    st.write("JSONファイルをアップロードしてください。")
