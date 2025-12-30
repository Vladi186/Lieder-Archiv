import streamlit as st
import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
import json
import os

st.set_page_config(page_title="Lieder-Archiv", layout="wide")

DB_FILE = "all_songs_ru.json"

def load_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except: return {}
    return {}

def save_data(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

db = load_data()

st.title("📚 Общий архив духовных песен")

# Блок поиска
search = st.text_input("🔍 Найти песню в архиве (введите название):")
if search:
    for title, content in db.items():
        if search.lower() in title.lower():
            with st.expander(f"📖 {title}"):
                c1, c2 = st.columns(2)
                c1.markdown("**Deutsch**")
                c1.write(content['original'])
                c2.markdown("**Русский**")
                c2.write(content['russian'])

st.divider()

# Блок добавления
st.subheader("📥 Добавить новую песню")
new_title = st.text_input("Название песни (например: Großer Gott):")
new_text = st.text_area("Вставьте текст песни здесь (Deutsch):")

if st.button("Сохранить и перевести"):
    if new_title and new_text:
        with st.spinner("Перевожу..."):
            translated = GoogleTranslator(source='auto', target='ru').translate(new_text)
            db[new_title] = {"original": new_text, "russian": translated}
            save_data(db)
            st.success(f"Песня '{new_title}' успешно добавлена!")
            st.rerun()
    else:
        st.warning("Пожалуйста, введите и название, и текст.")

st.write(f"📊 Песен в архиве: {len(db)}")
