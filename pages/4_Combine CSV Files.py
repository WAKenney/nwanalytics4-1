
import streamlit as st
import pandas as pd
import io
from datetime import datetime
from zoneinfo import ZoneInfo

# Create page title
titleCol1, titleCol2, titleCol3 = st.columns((1,4,1))
title = 'new_nw_header.png'
titleCol2.image(title, use_container_width=True)
st.subheader("Combine Multiple CSV Files")

with st.expander("Click here for help in getting started.", expanded=False):
    st.markdown("""This function provides a quick way to combine multiple CSV files 
                into a single Excel workbook for further analysis.
                In the "Drag and Drop" window below, select two or more CSV to combine. The app will 
                check the column titles for each of the files you have selected for consistency. If there are missing columns
                or inconsistent column names, the discrepancies will be shown. You will be given the opportunity to 
                proceed with the combination of the files or to exit the function to make changes to the column names and
                try again. Once you have successfully combined your files, click on the 
                'Download Concatenated Excel' button to save the new combined file.  The workbook will contain a required blank worksheet called 'streets' so that it can be used
                with NWAnalytics but you will have to add the street_code and street_name data to the file. 
                               
                """)

st.markdown("___")

# Initialize/reset uploader counter in session state if missing
if "upload_reset_counter" not in st.session_state:
    st.session_state.upload_reset_counter = 0

# Initialize session state keys if missing
for key in ["dataframes", "uploaded_files", "uploaded_filenames"]:
    if key not in st.session_state:
        st.session_state[key] = []

def clear_all():
    st.session_state.upload_reset_counter += 1
    for key in ["uploaded_files", "uploaded_filenames", "dataframes"]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

# Clear all button
if st.button("Clear All and Start Over"):
    clear_all()

# File uploader with dynamic key for reset
upload_key = f"uploaded_files_{st.session_state.upload_reset_counter}"

uploaded_files = st.file_uploader(
    "Select CSV Files to Concatenate",
    type="csv",
    accept_multiple_files=True,
    key=upload_key,
)

if uploaded_files:
    new_uploaded_filenames = [f.name for f in uploaded_files]
    cached_filenames = st.session_state.get("uploaded_filenames", [])
    if new_uploaded_filenames != cached_filenames:
        dfs = [pd.read_csv(f) for f in uploaded_files]
        st.session_state.uploaded_files = uploaded_files
        st.session_state.uploaded_filenames = new_uploaded_filenames
        st.session_state.dataframes = dfs
else:
    if "uploaded_files" not in st.session_state:
        st.session_state.uploaded_files = []
    if "uploaded_filenames" not in st.session_state:
        st.session_state.uploaded_filenames = []
    if "dataframes" not in st.session_state:
        st.session_state.dataframes = []

# Display previews and handle concatenation if data available
if st.session_state.dataframes:
    for idx, df in enumerate(st.session_state.dataframes):
        st.subheader(f"Preview of {st.session_state.uploaded_filenames[idx]}:")
        st.dataframe(df)

    cols_list = [set(df.columns) for df in st.session_state.dataframes]
    all_cols = set.union(*cols_list)
    mismatches = {}
    for i, cols in enumerate(cols_list):
        missing = all_cols - cols
        if missing:
            mismatches[f"{st.session_state.uploaded_filenames[i]} missing columns"] = missing

    if mismatches:
        st.warning("Column mismatches detected!")
        for file, missing_cols in mismatches.items():
            st.write(f"{file}: {', '.join(missing_cols)}")

        proceed = st.button("Proceed with concatenation anyway")
        exit_app = st.button("Exit without concatenating")
        if exit_app:
            st.stop()
        if proceed:
            concat_df = pd.concat(st.session_state.dataframes, ignore_index=True)
            st.subheader("Preview of Concatenated Data:")
            st.dataframe(concat_df)

            # Excel writer with 'trees' and 'streets'
            excel_buffer = io.BytesIO()
            with pd.ExcelWriter(excel_buffer, engine="xlsxwriter") as writer:
                concat_df.to_excel(writer, sheet_name="trees", index=False)
                pd.DataFrame(columns=["street_code", "street_name"]).to_excel(writer, sheet_name="streets", index=False)
            excel_bytes = excel_buffer.getvalue()

            st.download_button(
                label="Download Concatenated Excel (with trees & streets sheets)",
                data=excel_bytes,
                file_name="concatenated.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            st.markdown("""#### Reminder: The combined data workbook MUST include a worksheet called 'streets' if it is to be used with NWAnalytics.  The saved file has a 'streets' worksheet added but, you will have to add the necessary data in the 'street_code' and 'street_name' columns.
                        """)
    else:
        concat_df = pd.concat(st.session_state.dataframes, ignore_index=True)
        st.subheader("Preview of Concatenated Data:")
        st.dataframe(concat_df)

        # Excel writer with 'trees' and 'streets'
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine="xlsxwriter") as writer:
            concat_df.to_excel(writer, sheet_name="trees", index=False)
            pd.DataFrame(columns=["street_code", "street_name"]).to_excel(writer, sheet_name="streets", index=False)
        excel_bytes = excel_buffer.getvalue()

        # Create a timezone-aware current timestamp
        timestamp = datetime.now(ZoneInfo("America/New_York"))

        # Format the timestamp as a string with the desired date and time format
        formatted_timestamp = timestamp.strftime("%d-%m-%Y %H:%M:%S")

        # Use the formatted string in the filename
        st.download_button(
            label="📁 **Click here to download the combined file as an Excel file (with trees & streets sheets)** ",
            data=excel_bytes,
            file_name=f"combined file {formatted_timestamp}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        st.markdown("""#### Reminder: The combined data workbook MUST include a worksheet called 'streets' if it is to be used with NWAnalytics.  The saved file has a 'streets' worksheet added but, you will have to add the necessary data in the 'street_code' and 'street_name' columns.
                        """)
