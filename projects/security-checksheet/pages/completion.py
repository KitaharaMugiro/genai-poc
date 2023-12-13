import streamlit as st
import pandas as pd
import openai
import json
import requests

# StreamlitでExcelアップロードUI
st.title('AIセキュリティチェックシート回答ツール') 
group_name = "security-checksheet"
api_key = st.secrets["OPENAI_API_KEY"]
uploaded_file = st.file_uploader('Excelファイルを選択', type=['xlsx', 'xls'])

def extract_qa_chatgpt(df, row=0):
  questions = df.iloc[row].to_dict()
  questions_json = json.dumps(questions, ensure_ascii=False)
  prompt = questions_json + '''
  このセキュリティチェックシートの内容から、セキュリティチェックシートの質問を抽出してそのまま出力してください。
  '''
  response = openai.Completion.create(  
    engine="gpt-3.5-turbo-instruct", 
    prompt=prompt,
    max_tokens=3000,
  )
  return response.choices[0].text

def get_answer(q) : 
    system_prompt = """ユーザの質問に対して、必ず以下の情報を使って簡潔に答えてください。以下の情報に書かれていない場合は回答しないでください。

{{EMBEDDINGS_CONTEXT}}"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        max_tokens=3000,
        query=q ,
        groupName = group_name,
        headers = {
            "Content-Type": "application/json",
            "LangCore-Embeddings": "on",
            "LangCore-Embeddings-Match-Threshold": "0.5",
            "LangCore-Embeddings-Match-Count": "3",
        },
        messages= [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": q
                }
                ],
    )
    return response.choices[0].message.content

# 最初の10行を表示
if uploaded_file is not None:
  df = pd.read_excel(uploaded_file)
  # この内容をJSONにParse

  # とりあえず3行だけ読み込む
  qa_dataset = extract_qa_chatgpt(df, 8)
  st.write(qa_dataset)

  ans = get_answer(qa_dataset)
  st.write(ans)

  




