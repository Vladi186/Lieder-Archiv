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
search = st.text_input("🔍 Найти песню в архиве:")
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
url = st.text_input("Вставьте ссылку с evangeliums.net (необязательно):")
manual_title = st.text_input("Название (если по ссылке не найдет):")
manual_text = st.text_area("Текст песни (если по ссылке не найдет):")

if st.button("Сохранить и перевести"):
    final_title = ""
    final_text = ""
    
    # Пытаемся взять по ссылке
    if url:
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            res = requests.get(url, headers=headers)
            soup = BeautifulSoup(res.text, 'html.parser')
            final_title = soup.find('h1').text.strip()
            # Пробуем разные варианты поиска текста на сайте
            content_div = soup.find('div', class_='liedtext') or soup.find('div', class_='songtext')
            final_text = content_div.get_text(separator='\n').strip()
        except:
            st.error("По ссылке текст не найден. Использую ручной ввод.")
    
    # Если ссылка не сработала, берем ручной ввод
    if not final_title: final_title = manual_title
    if not final_text: final_text = manual_text
    
    if final_title and final_text:
        with st.spinner("Перевожу..."):
            translated = GoogleTranslator(source='auto', target='ru').translate(final_text)
            db[final_title] = {"original": final_text, "russian": translated}
            save_data(db)
            st.success(f"Песня '{final_title}' добавлена!")
            st.rerun()
    else:
        st.warning("Введите хотя бы ссылку или заполните поля вручную.")

st.write(f"📊 Песен в архиве: {len(db)}")
