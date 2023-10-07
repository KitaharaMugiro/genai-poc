# app.py
import streamlit as st
import geoip2.database
import requests


def get_location(ip_address, db_path):
    with geoip2.database.Reader(db_path) as reader:
        response = reader.city(ip_address)
        city = response.city.name
        return city


# クライアントのIPアドレスを取得
client_ip = st.text_input("Enter your IP address:", "")

if client_ip:
    db_path = "path_to_your_downloaded_mmdb_file"
    location = get_location(client_ip, db_path)
    st.write(f"Estimated location based on IP: {location}")
else:
    # クライアントのIPアドレスを取得するJavaScriptを実行
    st.markdown(
        """
        <script>
            async function setIP() {
                const ip = await fetchIP();
                const input = document.querySelector('input[type="text"]');
                input.value = ip;
                input.dispatchEvent(new Event('change', { 'bubbles': true }));
            }
            setIP();
        </script>
    """,
        unsafe_allow_html=True,
    )
