import streamlit as st
import json
import os
import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator

# Файл, где будут храниться ВСЕ песни
DB_FILE = 'songs_database.json'

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

st.set_page_config(page_title="Архив песен", layout="wide")
st.title("📚 Общий архив духовных песен")

songs_db = load_data()

# ПОИСК ПО ГОТОВОЙ БАЗЕ
search_query = st.text_input("🔍 Найти песню в нашем архиве (введите название):")
if search_query:
    results = [t for t in songs_db.keys() if search_query.lower() in t.lower()]
    if results:
        selected_song = st.selectbox("Найдено в архиве:", results)
        if selected_song:
            col1, col2 = st.columns(2)
            with col1:
                st.info(songs_db[selected_song]['de'])
            with col2:
                st.success(songs_db[selected_song]['ru'])
    else:
        st.warning("В архиве этой песни пока нет. Вы можете добавить её ниже!")

st.divider()

# ДОБАВЛЕНИЕ НОВОЙ ПЕСНИ (По ссылке)
st.subheader("📥 Добавить новую песню из evangeliums.net")
url_to_add = st.text_input("Вставь ссылку на новую песню:")

if st.button("Скачать в архив"):
    if url_to_add:
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            res = requests.get(url_to_add, headers=headers)
            res.encoding = 'utf-8'
            soup = BeautifulSoup(res.text, 'html.parser')
            
            title = soup.find('h1').text.strip() if soup.find('h1') else "Без названия"
            song_div = soup.find('div', class_='songtext') or soup.find('div', class_='liedtext')
            
            if song_div:
                text_de = song_div.get_text(separator='\n').strip()
                translator = GoogleTranslator(source='de', target='ru')
                text_ru = translator.translate(text_de)
                
                # Сохраняем в базу
                songs_db[title] = {"de": text_de, "ru": text_ru}
                save_data(songs_db)
                st.success(f"Песня '{title}' успешно добавлена в наш общий архив!")
                st.rerun()
            else:
                st.error("Не удалось забрать текст. Попробуйте скопировать его вручную.")
        except:
            st.error("Ошибка при обращении к сайту.")

# СТАТИСТИКА
st.sidebar.write(f"📊 Всего песен в архиве: {len(songs_db)}")