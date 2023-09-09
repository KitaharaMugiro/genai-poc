import openai
import streamlit as st
import os
from elevenlabs import generate, play, stream, set_api_key, VoiceSettings, Voice
from elevenlabs.api.error import UnauthenticatedRateLimitError, RateLimitError

def speak(text):
    try:
        audio = generate(text=text, 
                         voice=Voice(
                                voice_id='Ln9EThYHmy8oV6bISBUw',
                                settings=VoiceSettings(stability=0.71, similarity_boost=1, style=0.0, use_speaker_boost=True)
                            ),
                         model='eleven_multilingual_v2',
                         )
        st.audio(data=audio)
    except UnauthenticatedRateLimitError:
        e = UnauthenticatedRateLimitError("Unauthenticated Rate Limit Error")
        st.exception(e)

    except RateLimitError:
        e = RateLimitError('Rate Limit')
        st.exception(e)

st.title("LangCore Text2Speech")

openai.api_base = "https://oai.langcore.org/v1"
elevenlabs_api_key = os.environ.get("ELEVENLABS_API_KEY")
if elevenlabs_api_key:
    set_api_key(elevenlabs_api_key)
else :
    st.error("ELEVENLABS_API_KEY is not set")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Chat with my voice")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages= [
                {
                    "role": "system",
                    "content": "assistantはなるべく短く20文字以内で回答してください。長い回答になる場合は、無理やり短くしてください。"
                },
                *st.session_state.messages
                ],
                stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
    with st.spinner('Generating audio...'):
        speak(full_response)
