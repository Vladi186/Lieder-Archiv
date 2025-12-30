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
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

db = load_data()

st.title("📚 Мой архив духовных песен")

# Вывод списка песен по номерам
st.subheader("🎵 Список песен в архиве:")
if not db:
    st.info("Архив пока пуст. Добавьте первую песню ниже!")
else:
    # Сортируем песни, чтобы они шли по порядку
    for i, (title, content) in enumerate(db.items(), 1):
        with st.expander(f"№{i} - {title}"):
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**Deutsch**")
                st.write(content['original'])
            with c2:
                st.markdown("**Русский**")
                st.write(content['russian'])

st.divider()

# Блок ручного добавления (самый надежный)
st.subheader("📥 Добавить новую песню вручную")
new_title = st.text_input("Введите название песни:")
new_text = st.text_area("Вставьте немецкий текст:")

if st.button("Сохранить и перевести"):
    if new_title and new_text:
        with st.spinner("Перевожу..."):
            translated = GoogleTranslator(source='de', target='ru').translate(new_text)
            db[new_title] = {"original": new_text, "russian": translated}
            save_data(db)
            st.success(f"Песня №{len(db)} успешно добавлена!")
            st.rerun()
    else:
        st.warning("Заполните название и текст.")
