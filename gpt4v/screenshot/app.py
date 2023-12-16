import openai
import streamlit as st
import pyautogui
import os
import time
from gpt4v import gpt4v
from elevenlabs import generate, play, stream, set_api_key, VoiceSettings, Voice, voices
from elevenlabs.api.error import UnauthenticatedRateLimitError, RateLimitError

elevenlabs_api_key = os.environ.get("ELEVENLABS_API_KEY")
if elevenlabs_api_key:
    set_api_key(elevenlabs_api_key)
else :
    st.error("ELEVENLABS_API_KEY is not set")

def autoplay_audio(file_path: str):
    import base64
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio controls autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(
            md,
            unsafe_allow_html=True,
        )

def speak(text, voice):
    try:
        audio = generate(text=text, 
                         voice=Voice(
                                voice_id=voice,
                                settings=VoiceSettings(stability=0.71, similarity_boost=1, style=0.0, use_speaker_boost=True)
                            ),
                         model='eleven_multilingual_v2'
                         )
        # byteをファイルに書き込む
        audio_path = "audio.mp3"
        with open(audio_path, mode="wb") as f:
            f.write(audio) # type: ignore

        autoplay_audio(audio_path)
    except UnauthenticatedRateLimitError:
        e = UnauthenticatedRateLimitError("Unauthenticated Rate Limit Error")
        st.exception(e)

    except RateLimitError:
        e = RateLimitError('Rate Limit')
        st.exception(e)


# Streamlitアプリのタイトルを設定
st.title("スクリーンショットから会話を考える")
INTERVAL = 3

# 作業ディレクトリのパスを取得
working_directory = os.getcwd()
filename = os.path.join(working_directory, "screenshot.png")

# スクリーンショットの表示エリアを初期化
placeholder = st.empty()

# スタートとストップの状態を管理する変数
start = False
stop = False
runnning = False
# スタートボタン
if st.button("スクリーンショットを自動更新開始", key="start"):
    start = True
    runnning = False

# ストップボタン
if st.button("停止", key="stop"):
    stop = True

# 自動更新のループ
while start and not stop and not runnning:
    running = True
    # 待機
    time.sleep(INTERVAL)

    # スクリーンショットを取得し、ファイルに保存
    screenshot = pyautogui.screenshot()
    screenshot.save(filename)
    speak("ふむふむ・・・", "Z4mJYxrYLXWVp55j0Swf")

    # # スクリーンショットの画像を表示
    # placeholder.image(filename)

    # ストップフラグを確認
    stop = st.session_state.get("stop", False)

    # API呼び出し
    res = gpt4v(filename, st.secrets["OPENAI_API_KEY"])
    st.write(res)
    with st.spinner('Generating audio...'):
        speak(res, "Z4mJYxrYLXWVp55j0Swf")
    running = False


if stop:
    st.write("自動更新が停止されました。")