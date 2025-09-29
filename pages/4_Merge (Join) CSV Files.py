import streamlit as st
import pandas as pd

st.title("Concatenate Multiple CSV Files")

# Upload CSV files (accepts multiple files)
uploaded_files = st.file_uploader(
    "Select CSV Files to Concatenate", 
    type="csv", 
    accept_multiple_files=True
)

if uploaded_files:
    dataframes = []
    for uploaded_file in uploaded_files:
        # Read each CSV into a DataFrame
        df = pd.read_csv(uploaded_file)
        dataframes.append(df)
        st.write(f"Preview of {uploaded_file.name}:")
        st.dataframe(df)
    
    # Concatenate all DataFrames, stacking their rows
    concatenated_df = pd.concat(dataframes, ignore_index=True)
    
    st.write("Preview of Concatenated CSV:")
    st.dataframe(concatenated_df)

    # Download concatenated CSV
    csv = concatenated_df.to_csv(index=False)
    st.download_button(
        label="Download Concatenated CSV",
        data=csv,
        file_name="concatenated.csv",
        mime="text/csv"
    )