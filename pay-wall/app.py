import openai
import streamlit as st
from st_paywall import add_auth


openai.api_base = "https://oai.langcore.org/v1"
st.title("タイトル")

add_auth(required=True)

st.write("認証が必要なコンテンツ")
# after authentication, the email and subscription status is stored in session state
st.write(st.session_state.email)
st.write(st.session_state.user_subscribed)
