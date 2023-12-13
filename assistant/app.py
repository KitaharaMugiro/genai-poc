import openai
import streamlit as st
from openai import OpenAI


st.title("数学の問題をコードで解く")

client = OpenAI()

if st.button("数学の問題を解く"):

    # アシスタントを作成
    assistant = client.beta.assistants.create(
        name="mugiro",
        instructions="write a code",
        tools=[{"type": "code_interpreter"}],
        model="gpt-4-1106-preview"
    )
    st.write("アシスタントを新規作成")
    st.write(assistant)

    # スレッドを作成
    thread = client.beta.threads.create(
        messages=[
            {
            "role": "user",
            "content": "I need to solve the equation `3x + 11 = 14`. Can you help me?"
            }
        ]
)
    st.write("スレッドを新規作成")
    st.write(thread)

    # スレッドを実行
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions="write a code and get the answer"
    )
    st.write("スレッドを実行")
    st.write(run.status)
    
    ## まつ
    import time
    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        st.write(run.status)
        time.sleep(1)


    # メッセージを取得
    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )
    st.write("メッセージを取得")
    st.write(messages.data[0].content[0].text.value)

    # アシスタントの削除
    client.beta.assistants.delete(
        assistant_id=assistant.id
    )