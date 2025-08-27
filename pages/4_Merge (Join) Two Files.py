import streamlit as st
import pandas as pd


#Create page title
titleCol1, titleCol2, titleCol3 =st.columns((1,4,1))

title = 'new_nw_header.png'

titleCol2.image(title, use_container_width=True)
# titleCol2.image(title, use_column_width=True)

st.subheader('Merge (join) Two or More CSV Files')

st.markdown("___")

message_screen = st.empty()
st.markdown("___")

screen1 = st.empty()
screen2 = st.empty()
screen3 = st.empty()
screen4 = st.empty()

message_screen.write("Hi there")

# File1 uploader
file1_name = screen2.file_uploader("Choose a CSV file", type=["csv"])

# Check if a file has been uploaded
if file1_name is not None:
    # Read the CSV into a DataFrame
    file1 = pd.read_csv(file1_name)

    # Display the DataFrame
    screen1.write("Here is your uploaded data:")
    screen2.dataframe(file1)  # Streamlit interactive table

    message_screen.write("Now scroll down and select a csv file to merge with the one ou just selected.")


    if file1_name is not None:
        # File2 uploader
        file2_name = screen3.file_uploader("Choose the CSV file to be merged with the first file", type=["csv"])

        # Check if a file has been uploaded
        if file2_name is not None:
            # Read the CSV into a DataFrame
            file2 = pd.read_csv(file2_name)

            # Display the DataFrame
            st.write("Here is your second uploaded data:")
            st.dataframe(file2)  # Streamlit interactive table

        if file2_name is not None:

            st.header("Concatenated")
            result = pd.concat([file1, file2])
            st.dataframe(result)

            duplicates = result[result.duplicated(keep=False)]

            if not duplicates.empty:
                st.header("Duplicates")
                st.dataframe(duplicates)

            
            st.markdown("___")

            left, right = st.columns(2)

            if left.button("Click here to merge another file"):
                left.markdown("You clicked the plain button.")
            
            
            if right.button("Click here to save the merged file to your computer"):
                right.markdown("You clicked the Material button.")

        @st.cache_data
        def save_result(result):  
            return result.to_csv().encode("utf-8")
        

        csv = save_result(result)

        # Ask for filename input
        # default_filename = "merged_files.csv"

        filename = st.text_input("Enter filename for CSV (including .csv)")

        st.download_button(
            label=':floppy_disk: Click here to save your data on your local computer',
            data=csv,
            file_name=filename,
            mime="text/csv",
        )

    else:
        st.info("Please upload the CSV file to be merged with the first.")

else:
    screen1.info("Please upload a CSV file in the box below.")
