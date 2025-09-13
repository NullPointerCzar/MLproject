import streamlit as st
from preprocessor import preprocess
from helper import fetch_stats


st.sidebar.title("WhatsApp Chat Analyzer")

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df, df_cleaned = preprocess(data)
    
    st.dataframe(df)
    unique_names = df_cleaned['Name'].unique().tolist()
    unique_names.insert(0, 'Overall')
    selected_user = st.sidebar.selectbox("Show analysis wrt", unique_names)

    if st.sidebar.button("Show Analysis"):

        num_messages = fetch_stats(selected_user, df)


        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
