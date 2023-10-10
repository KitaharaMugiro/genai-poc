import openai
import streamlit as st
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
import os

cognitive_service_url = os.environ.get("COGNITIVE_SERVICE_URL")
cognitive_service_key = os.environ.get("COGNITIVE_SERVICE_KEY")
openai.api_base = "https://oai.langcore.org/v1"
def main():
    st.title('問題自動作成')
    file_path = st.file_uploader("画像ファイル(png)をアップロード", type=["png"])
    if file_path is not None:
        st.image(file_path)
        st.write(file_path)
        document_analysis_client = DocumentAnalysisClient(endpoint=cognitive_service_url, credential=AzureKeyCredential(cognitive_service_key))

        file_bytes = file_path.read()  # ここで読み込む
        poller = document_analysis_client.begin_analyze_document("prebuilt-document", file_bytes)
        form_recognizer_results = poller.result()

        if form_recognizer_results:
            page_text = ""
            for page_num, page in enumerate(form_recognizer_results.pages):
                tables_on_page = [table for table in form_recognizer_results.tables if
                                table.bounding_regions[0].page_number == page_num + 1]

                # mark all positions of the table spans in the page
                page_offset = page.spans[0].offset
                page_length = page.spans[0].length
                table_chars = [-1] * page_length
                for table_id, table in enumerate(tables_on_page):
                    for span in table.spans:
                        # replace all table spans with "table_id" in table_chars array
                        for i in range(span.length):
                            idx = span.offset - page_offset + i
                            if idx >= 0 and idx < page_length:
                                table_chars[idx] = table_id
                # build page text by replacing charcters in table spans with table html
                page_text = ""
                added_tables = set()
                for idx, table_id in enumerate(table_chars):
                    if table_id == -1:
                        page_text += form_recognizer_results.content[page_offset + idx]
                    elif not table_id in added_tables:
                        pass
                        #page_text += table_to_html(tables_on_page[table_id])
                        #added_tables.add(table_id)

                page_text += " "

            # st.write(page_text[:4000])

            res = openai.ChatCompletion.create(
                model="gpt-4",
                temperature=0,
                messages=[
                    {
                        "role": "system",
                        "content": """ノートの内容を与えるので、そこから穴埋め問題を作成してください。対象者は日本人の中学生です。日本語で問題を作成してください。
                        以下の制約を守ってください。
                        1. 正解があること
                        2. 問題文から答えが推測されないこと
                        """
                    },
                    {
                        "role": "user",
                        "content": page_text[:4000]
                    }
                ]
            )
            ai_response = res.choices[0].message.content
            st.write(ai_response)

if __name__ == '__main__':
    main()
