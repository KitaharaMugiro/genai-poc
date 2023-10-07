# app.py
import streamlit as st
import geoip2.database
import requests


def get_location(ip_address, db_path):
    with geoip2.database.Reader(db_path) as reader:
        response = reader.city(ip_address)
        city = response.city.name
        return city


def get_ip():
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get("https://httpbin.org/ip", headers=headers)
    return response.json()["origin"]


st.title("IPアドレスに基づく位置情報推定アプリ")

ip_address = get_ip()
st.write(f"Your IP address is: {ip_address}")

db_path = "./GeoLite2-City.mmdb"  # こちらを実際のデータベースファイルのパスに変更してください
location = get_location(ip_address, db_path)
st.write(f"Estimated location based on IP: {location}")
