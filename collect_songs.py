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
    # Сортируем базу по названию перед сохранением
    sorted_data = dict(sorted(data.items()))
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(sorted_data, f, ensure_ascii=False, indent=4)

db = load_data()

st.title("📚 Большой архив духовных песен")

# --- СЕКЦИЯ ПОИСКА ---
st.subheader("🔍 Быстрый поиск")
search_query = st.text_input("Введите номер или часть названия песни:")

# --- ВЫВОД ПЕСЕН ---
if db:
    # Фильтруем песни по поиску
    filtered_songs = []
    for i, (title, content) in enumerate(db.items(), 1):
        display_title = f"№{i} - {title}"
        if search_query.lower() in display_title.lower():
            filtered_songs.append((display_title, content))

    if filtered_songs:
        for title, content in filtered_songs:
            with st.expander(title):
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("**Deutsch**")
                    st.write(content['original'])
                with c2:
                    st.markdown("**Русский**")
                    st.write(content['russian'])
    else:
        st.warning("Песня не найдена.")
else:
    st.info("Архив пуст.")

st.divider()

# --- СЕКЦИЯ ДОБАВЛЕНИЯ ---
st.subheader("📥 Добавить в библиотеку")
with st.form("add_form", clear_on_submit=True):
    new_title = st.text_input("Название песни:")
    new_text = st.text_area("Текст на немецком:")
    submit = st.form_submit_button("Добавить в архив")

    if submit:
        if new_title and new_text:
            with st.spinner("Перевод и сохранение..."):
                try:
                    translated = GoogleTranslator(source='de', target='ru').translate(new_text)
                    db[new_title] = {"original": new_text, "russian": translated}
                    save_data(db)
                    st.success(f"Песня '{new_title}' успешно добавлена!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Ошибка: {e}")
        else:
            st.warning("Заполните оба поля.")

st.write(f"📊 Всего в базе: {len(db)} из 1311+")
