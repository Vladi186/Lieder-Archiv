import streamlit as st
import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
import json
import os

st.set_page_config(page_title="Архив песен", layout="wide")

DB_FILE = "all_songs_ru.json"

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

db = load_data()

st.title("📚 Общий архив духовных песен")

# Поиск
search = st.text_input("🔍 Найти песню в нашем архиве:")
if search:
    results = {k: v for k, v in db.items() if search.lower() in k.lower()}
    for title, content in results.items():
        with st.expander(f"📖 {title}"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Deutsch**")
                st.write(content['original'])
            with col2:
                st.markdown("**Русский**")
                st.write(content['russian'])

st.divider()

# Добавление
st.subheader("📥 Добавить новую песню")
url = st.text_input("1. Вставьте ссылку с evangeliums.net:")
manual_text = st.text_area("2. Если текст не загрузился автоматически, вставьте его сюда вручную:")

if st.button("Скачать и перевести"):
    song_text = ""
    song_title = "Новая песня"
    
    if manual_text:
        song_text = manual_text
    elif url:
        try:
            res = requests.get(url)
            soup = BeautifulSoup(res.text, 'html.parser')
            song_text = soup.find('div', class_='liedtext').get_text(separator='\n')
            song_title = soup.find('h1').text.strip()
        except:
            st.error("Не удалось забрать текст по ссылке. Вставьте его вручную в поле выше.")
    
    if song_text:
        with st.spinner("Перевожу..."):
            translated = GoogleTranslator(source='auto', target='ru').translate(song_text)
            db[song_title] = {"original": song_text, "russian": translated}
            save_data(db)
            st.success(f"Песня '{song_title}' сохранена!")
            st.rerun()

st.write(f"📊 Всего песен в архиве: {len(db)}")
