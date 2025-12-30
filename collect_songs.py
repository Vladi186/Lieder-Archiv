import streamlit as st
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
    # Сортируем базу по числовому номеру перед сохранением
    sorted_data = dict(sorted(data.items(), key=lambda item: int(item[0]) if item[0].isdigit() else 9999))
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(sorted_data, f, ensure_ascii=False, indent=4)

db = load_data()

st.title("📚 Духовный песенник (1311+)")

# --- СЕКЦИЯ ПОИСКА ---
st.subheader("🔍 Поиск по номеру или названию")
search_query = st.text_input("Введите номер (например, 120) или слово:")

# --- ВЫВОД ПЕСЕН ---
if db:
    # Фильтруем песни по поиску
    for song_id, content in db.items():
        display_name = f"№{song_id} - {content['title']}"
        if search_query.lower() in display_name.lower() or search_query == song_id:
            with st.expander(display_name):
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("**Deutsch**")
                    st.write(content['original'])
                with c2:
                    st.markdown("**Русский**")
                    st.write(content['russian'])
else:
    st.info("Архив пуст. Добавьте первую песню ниже.")

st.divider()

# --- СЕКЦИЯ ДОБАВЛЕНИЯ ---
st.subheader("📥 Добавить песню в архив")
with st.form("add_form", clear_on_submit=True):
    col_num, col_name = st.columns([1, 4])
    with col_num:
        song_num = st.text_input("№") # Поле для номера
    with col_name:
        song_title = st.text_input("Название песни")
    
    song_text = st.text_area("Текст на немецком")
    submit = st.form_submit_button("Сохранить в архив")

    if submit:
        if song_num and song_title and song_text:
            with st.spinner("Перевожу и сохраняю..."):
                try:
                    translated = GoogleTranslator(source='de', target='ru').translate(song_text)
                    # Сохраняем, где ключ — это номер песни
                    db[song_num] = {
                        "title": song_title,
                        "original": song_text,
                        "russian": translated
                    }
                    save_data(db)
                    st.success(f"Песня №{song_num} успешно добавлена!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Ошибка: {e}")
        else:
            st.warning("Пожалуйста, заполните номер, название и текст.")

st.write(f"📊 Песен в базе: {len(db)}")
