import openai
import streamlit as st
import json

openai.api_base = "https://oai.langcore.org/v1"

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
        return res["function_call"]["arguments"]
    return res


def main():
    st.title("Function Calling Usecase Demo")


if __name__ == "__main__":
    main()