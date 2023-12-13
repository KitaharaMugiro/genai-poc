import streamlit as st
import pandas as pd
import openai
import json
import requests

# StreamlitでExcelアップロードUI
st.title('AIセキュリティチェックシート登録ツール') 
api_key = st.secrets["OPENAI_API_KEY"]
uploaded_file = st.file_uploader('Excelファイルを選択', type=['xlsx', 'xls'])

def extract_qa_chatgpt(df, from_row=0, to_row=10):
  questions = df[from_row:to_row].to_dict(orient="records")
  questions_json = json.dumps(questions, ensure_ascii=False)
  prompt = questions_json + '''
  このセキュリティチェックシートの内容を読んで、以下のようなJSON形式にまとめてください
  EXAMPLE: [{"q": "質問1", "a": "回答1"}, {"q": "質問2", "a": "回答2"}]
  OUTPUT: 
  '''
  response = openai.Completion.create(  
    engine="gpt-3.5-turbo-instruct", 
    prompt=prompt,
    max_tokens=3000,
  )
  return json.loads(response.choices[0].text)

# 最初の10行を表示
if uploaded_file is not None:
  df = pd.read_excel(uploaded_file)
  # この内容をJSONにParse

  # とりあえず18行だけ読み込む
  qa_dataset1 = extract_qa_chatgpt(df, 0, 8)
  qa_dataset2 = extract_qa_chatgpt(df, 9, 18)

  qa_dataset = qa_dataset1 + qa_dataset2 
  # dataframeテーブル形式で表示
  df = pd.DataFrame(qa_dataset)
  st.write(df)

  # データベースに登録
  def embed_text_with_openai(api_key, text, metadata, groupName="default"):
    url = "http://langcore.org/api/embeddings"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {"input": text, "groupName": groupName, "metadata": metadata}

    response = requests.post(url, json=data, headers=headers)

    if response.status_code != 200:
        st.error(f"Error {response.status_code}: {response.text}")
        return None
    return response.json()
  
  for qa in qa_dataset:
    embed_text_with_openai(api_key, qa["q"], qa["a"], "security-checksheet")




