import streamlit as st
import scraper
import ai_processor

st.title("Поиск характеристик оборудования")

code = st.text_input("Код модели (например, ГНОМ 40-25)")
field1 = st.text_input("Поле №1 (например, Насосы)")
field2 = st.text_input("Поле №2 (например, Погружные)")

if st.button("Найти характеристики"):
    if code and field1 and field2:
        with st.spinner("Поиск данных..."):
            # Шаг 1: поиск данных в интернете
            raw_data = scraper.search_equipment_specs(code, field1, field2)
            # Шаг 2: обработка нейросетью
            processed_data = ai_processor.extract_specs_with_ai(raw_data, code, field1, field2)
            # Шаг 3: отображение таблицы
            st.write("Результаты поиска:")
            if not processed_data.empty:
                st.dataframe(processed_data)
            else:
                st.info("Характеристики не найдены. Попробуйте другой код или уточните запрос.")
    else:
        st.error("Заполните все поля!")