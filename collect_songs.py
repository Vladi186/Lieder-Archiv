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

# 1. ПОИСК
st.subheader("🔍 Поиск в твоём архиве")
search = st.text_input("Введите название песни для поиска:")
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

# 2. ДОБАВЛЕНИЕ
st.subheader("📥 Добавить новую песню")

# Поле для ссылки
input_url = st.text_input("Вариант А: Вставьте ссылку на песню (evangeliums.net):")

st.write("--- ИЛИ ---")

# Поля для ручного ввода
manual_title = st.text_input("Вариант Б: Введите название вручную:")
manual_text = st.text_area("Вариант Б: Вставьте немецкий текст вручную:")

if st.button("🚀 Сохранить и перевести"):
    final_title = ""
    final_text = ""
    
    # Сначала пробуем ссылку
    if input_url:
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            res = requests.get(input_url, headers=headers, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            
            # Пробуем найти заголовок
            h1 = soup.find('h1')
            if h1: final_title = h1.text.strip()
            
            # Пробуем найти текст (разные варианты верстки сайта)
            content_div = soup.find('div', class_='liedtext') or soup.find('div', class_='songtext')
            if content_div:
                final_text = content_div.get_text(separator='\n').strip()
        except:
            st.error("Не удалось скачать по ссылке автоматически.")

    # Если ссылка не дала данных, берем ручные поля
    if not final_title: final_title = manual_title
    if not final_text: final_text = manual_text

    if final_title and final_text:
        with st.spinner("Перевожу на русский..."):
            try:
                translated = GoogleTranslator(source='de', target='ru').translate(final_text)
                db[final_title] = {"original": final_text, "russian": translated}
                save_data(db)
                st.success(f"Песня '{final_title}' успешно сохранена!")
                st.rerun()
            except Exception as e:
                st.error(f"Ошибка при переводе: {e}")
    else:
        st.warning("Пожалуйста, заполните либо ссылку, либо название и текст.")

st.divider()
st.write(f"📊 Песен в архиве: {len(db)}")
