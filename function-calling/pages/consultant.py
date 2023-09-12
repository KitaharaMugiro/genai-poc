import openai
import streamlit as st
import json

openai.api_base = "https://oai.langcore.org/v1"

def write_spreadsheet(question:str, answer:str):
    st.success("以下の情報をスプレッドシートに保存します")
    st.json({
        "userId": "test-user-id",
        "question": question,
        "answer": answer
    })

def function_calling(messages, functions, function_name):
    function_call = "auto"
    if function_name: 
        function_call = {"name": function_name}
    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            functions=functions,
            function_call=function_call
    )

    assert "choices" in response, response
    res = response["choices"][0]["message"] # type: ignore
    if "function_call" in res:
        return json.loads(res["function_call"]["arguments"]), True
    return res, False

def system_prompt(question): 
    return f"""
    ロール:
    あなたは社会人向けのキャリアコーチです。ユーザの深層心理を引き出してください。

    行動:
    1.まず、[質問]のあとに書かれている質問をユーザにしてください。
    2.ユーザの回答が不十分だと感じられる場合は、深掘りをする質問をしてください。
    3.[質問]に対する回答を引き出せたと感じたら、end_question関数を呼び出してください。
    4.しつこい深堀はしないでください。また[質問]から逸脱しないでください。

    [質問] 
    {question} 
    """

def functions(question):
    return [
    {
            "name": "end_question", 
            "description": "深掘りを完了した時に呼び出す関数", 
            "parameters": {
                "type": "object",
                "properties": {
                    "answer": {
                        "type": "string",
                        "description": f"[{question}]に対するユーザの回答会話履歴を全部見てを100文字程度でまとめてください。", 
                    },
                },
                "required": [ "answer"], 
            },
        }
    ]

def main():
    st.title("キャリアコンサルタント PoC")
    st.text("対話を通して深層心理を導き、スプレッドシートに保存します")
    question = st.text_input("聞きたい質問", value="あなたが決断するときに，大事にしていることは何ですか？")
    
    # states
    if st.session_state == {}:
        st.session_state.messages = []
        st.session_state.attempts = 0


    

    user_answer = st.text_input("あなたの回答:")
    if st.button("回答する"):
        st.session_state.messages.append({"role": "user", "content": user_answer})
        # loading
        with st.spinner("AIが考え中..."):
            res, is_end = function_calling([ {"role": "system", "content": system_prompt(question)}, *st.session_state.messages], functions(question), None)            
        if is_end:
            write_spreadsheet(question, res["answer"])
        else:
            st.session_state.attempts += 1
            if st.session_state.attempts < 3:
                st.info(res["content"])
                st.session_state.messages.append({"role": "assistant", "content": res["content"]})
            else:
                res, is_end = function_calling([ {"role": "system", "content": system_prompt(question)}, *st.session_state.messages], functions(question), "end_question")
                write_spreadsheet(question, res["answer"])


if __name__ == "__main__":
    main()