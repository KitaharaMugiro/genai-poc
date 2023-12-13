import openai
import streamlit as st
from openai import OpenAI


st.title("タイトル")

client = OpenAI(base_url = "https://oai.langcore.org/v1")

if st.button("猫の画像を作る"):
    response = client.images.generate(
        model="dall-e-3",
        prompt="a white siamese cat",
        size="1024x1024",
        quality="standard",
        n=1,
        )

    image_url = response.data[0].url
    st.image(image_url, width=300)

    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "写真の中に何が映ってる？"},
                    {
                        "type": "image_url",
                        "image_url": image_url,
                    },
                ],
            }
        ],
        max_tokens=300,
    )

    st.write(response.choices[0].message.content)