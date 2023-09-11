from pytube import YouTube
import os
import streamlit as st
from elevenlabs import clone, generate, set_api_key, VoiceSettings, Voice

white_list = ["test@localhost.com", "adapp.mail@gmail.com"]
st.write(st.experimental_user.email)
if st.experimental_user.email not in white_list: 
	st.stop()

elevenlabs_api_key = os.environ.get("ELEVENLABS_API_KEY")
if elevenlabs_api_key:
    set_api_key(elevenlabs_api_key)
    
@st.cache_data
def save_audio(url):
	yt = YouTube(url)
	video = yt.streams.filter(only_audio=True).first()
	if video is None:
		raise ValueError("No audio stream found for this video")

	out_file = video.download()
	# out_fileのディレクトリを取得
	directory = os.path.dirname(out_file)

	# ディレクトリと新しいファイル名を結合して最終的なパスを取得
	final_path = os.path.join(directory, 'output.mp3')
	# out_fileをoutput.mp3にリネーム
	os.rename(out_file, 'output.mp3')

	print(yt.title + " has been successfully downloaded.")
	return yt.title, final_path, yt.thumbnail_url

st.title('Youtube Clone')
url = st.text_input('URL', key='url')
name = st.text_input('Name', key='name')

voice = st.session_state.get('voice', None)
if st.button('Clone'):
	title, file_name, thumbnail_url = save_audio(url)	
	# 音声分離したい	
	voice = clone(
		name=name,
		files=[file_name],
	)
	st.session_state['voice'] = voice


if voice: 
	text = st.text_input('Text', key='text')
	create = st.button('Create')
	if create:
		audio = generate(text=text, voice=Voice(
                                voice_id=voice.voice_id,
                                settings=VoiceSettings(stability=0.71, similarity_boost=1, style=0.0, use_speaker_boost=True)
                            ),
                         model='eleven_multilingual_v2')
		st.audio(audio)
