import streamlit as st
import pandas as pd


# File upload for the first DataFrame
st.subheader("Upload first CSV file")
file1 = st.file_uploader("Choose a CSV file", key="file1")
df1 = pd.read_csv(file1)

st.dataframe(df1)

# File upload for the second DataFrame
st.subheader("Upload second CSV file")
file2 = st.file_uploader("Choose a CSV file", key="file2")
df2 = pd.read_csv(file2)

st.dataframe(df2)

st.header("Concatenated")
result = pd.concat([df1, df2])
st.dataframe(result)

st.header("Duplicates")
duplicates = result[result.duplicated(keep=False)]

st.dataframe(duplicates)


@st.cache_data
def convert_result(result):  
    return result.to_csv().encode("utf-8")

csv = convert_result(result)

st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name="large_df.csv",
    mime="text/csv",
)