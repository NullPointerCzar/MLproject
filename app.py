import streamlit as st
from preprocessor import preprocess


st.sidebar.title("WhatsApp Chat Analyzer")

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocess(data)
    
    st.dataframe(df)