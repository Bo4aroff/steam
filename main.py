import pandas as pd
import streamlit as st
import base64
from io import StringIO, BytesIO
from openpyxl import Workbook



def generate_excel_download_link(df_2):
    # Credit Excel: https://discuss.streamlit.io/t/how-to-add-a-download-excel-csv-function-to-a-button/4474/5
    towrite = BytesIO()
    df.to_excel(towrite, encoding="utf-8", index=False, header=True)  # write to BytesIO buffer
    towrite.seek(0)  # reset pointer
    b64 = base64.b64encode(towrite.read()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="data_download.xlsx">Download Excel File</a>'
    return st.markdown(href, unsafe_allow_html=True)


st.set_page_config(page_title='Search_words')
st.title('Excel Plotter')
st.subheader('Перенесите свой Excel файл')

uploaded_file = st.file_uploader('ВЫБИРИТЕ СВОЙ ФАЙЛ', type='xlsx')
if uploaded_file:
    st.markdown('---')
    df = pd.read_excel(uploaded_file, engine='openpyxl')
    df['История заболевания'] = df['История заболевания'].astype(str)
    st.dataframe(df)



with st.form('Search'):
    keyword_ = st.text_input('Введите слово')
    keyword_two = st.text_input('Введите слово 2')
    keyword_three = st.text_input('Введите слово 3')
    search = st.form_submit_button("Поиск")
    if search:
        def identify_subject(df, refs):
            flag = 0
            for ref in refs:
                if df.find(ref) != -1:
                    flag = 1
            return flag

        step_one = [keyword_]
        step_two = [keyword_two]
        step_three = [keyword_three]

        df['Введеное слово'] = df['История заболевания'].apply(lambda x: identify_subject(x, step_one))
        df['Введеное слово 2'] = df['История заболевания'].apply(lambda x: identify_subject(x, step_two))
        df['Введеное слово 3'] = df['История заболевания'].apply(lambda x: identify_subject(x, step_three))


df_2 = st.dataframe(df)

st.subheader('СКАЧАТЬ ФАЙЛ')
generate_excel_download_link(df_2)