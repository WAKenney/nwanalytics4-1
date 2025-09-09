import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Merge CSV Files", layout="centered")

#Create page title
titleCol1, titleCol2, titleCol3 =st.columns((1,4,1))

title = 'new_nw_header.png'

titleCol2.image(title, use_container_width=True)

st.header('📂 Merge (join) Two or More CSV Files')

st.markdown("___")

message_screen = st.empty()
st.markdown("___")

screen1 = st.empty()
screen2 = st.empty()
screen3 = st.empty()
screen4 = st.empty()
screen5 = st.empty()
# screen6 = st.empty()

# --- Session State Initialization ---
if "file1" not in st.session_state:
    st.session_state.file1 = None
if "df1" not in st.session_state:
    st.session_state.df1 = None
if "file2" not in st.session_state:
    st.session_state.file2 = None
if "df2" not in st.session_state:
    st.session_state.df2 = None
if "merged" not in st.session_state:
    st.session_state.merged = None

def display_file(file, df, label):
    st.success(f"✅ {label} uploaded: {file.name}")
    st.subheader(f"Preview {label}")
    st.dataframe(df)
    st.download_button(f"💾 Download {label}", data=file.getvalue(), file_name=file.name)
    if st.button(f"Replace {label}"):
        # Clear selected file and its DataFrame from session state
        st.session_state[f"file{label[-1]}"] = None
        st.session_state[f"df{label[-1]}"] = None
        st.session_state.merged = None

# --- Upload File 1 ---
st.header("Step 1: Upload First File")
if st.session_state.file1 is None:
    uploaded_file1 = st.file_uploader("Upload your first CSV file", type=["csv"], key="upload1")
    if uploaded_file1:
        try:
            df1 = pd.read_csv(uploaded_file1)
            st.session_state.file1 = uploaded_file1
            st.session_state.df1 = df1
        except Exception as e:
            st.error(f"Error reading first file as CSV: {e}")
else:
    display_file(st.session_state.file1, st.session_state.df1, "File 1")

st.divider()

# --- Upload File 2 ---
st.header("Step 2: Upload Second File")
if st.session_state.file1:  # Only allow File 2 upload if File 1 exists
    if st.session_state.file2 is None:
        uploaded_file2 = st.file_uploader("Upload your second CSV file", type=["csv"], key="upload2")
        if uploaded_file2:
            try:
                df2 = pd.read_csv(uploaded_file2)
                st.session_state.file2 = uploaded_file2
                st.session_state.df2 = df2
            except Exception as e:
                st.error(f"Error reading second file as CSV: {e}")
    else:
        display_file(st.session_state.file2, st.session_state.df2, "File 2")

st.divider()

# --- Merge Option ---
if st.session_state.df1 is not None and st.session_state.df2 is not None:
    st.header("Step 3: Merge Files")
    if st.button("🔄 Merge Files"):
        try:
            merged_df = pd.concat([st.session_state.df1, st.session_state.df2], ignore_index=True)
            st.session_state.merged = merged_df
            st.success("✅ Files merged successfully!")
        except Exception as e:
            st.error(f"⚠️ Unable to merge: {e}")

# --- Show merged result + save option ---
if st.session_state.merged is not None:
    st.subheader("🔍 Preview Merged File")
    st.dataframe(st.session_state.merged)

    filename = st.text_input("Enter filename for merged file", "merged.csv")
    if filename:
        buffer = io.BytesIO()
        st.session_state.merged.to_csv(buffer, index=False)
        st.download_button(
            "💾 Download Merged File",
            data=buffer.getvalue(),
            file_name=filename,
            mime="text/csv"
        )







# import streamlit as st
# import pandas as pd
# import uuid

# #Create page title
# titleCol1, titleCol2, titleCol3 =st.columns((1,4,1))

# title = 'new_nw_header.png'

# titleCol2.image(title, use_container_width=True)
# # titleCol2.image(title, use_column_width=True)

# st.header('Merge (join) Two or More CSV Files')

# st.markdown("___")

# message_screen = st.empty()
# st.markdown("___")

# screen1 = st.empty()
# screen2 = st.empty()
# screen3 = st.empty()
# screen4 = st.empty()
# screen5 = st.empty()
# screen6 = st.empty()

# if "uploader_key" not in st.session_state:
#     st.session_state.uploader_key = 0


# # @st.cache_data
# def file_uploader():
#     # key = st.session_state.uploader_key+1
#     st.session_state.uploader_key = st.session_state.uploader_key+1
#     file_name = screen2.file_uploader("Choose a CSV file", type=["csv"])
#     data = pd.read_csv(file_name)
#     return data


# def merge_files(file1, file2):
#     return pd.concat([file1, file2])


# def save_result(result):  
#     return result.to_csv().encode("utf-8")


# file1= file_uploader()

# st.write(file1)

# left, right = st.columns(2)

# if left.button("This is NOT the right file? Click here to try again"):
#     file1= file_uploader()

#     st.write(file1)
















# if right.button("Yes, this is the correct file. CONTINUE"):
#     right.markdown("You clicked the Material button.")




# file1_name = screen2.file_uploader("Choose a CSV file", type=["csv"])

# Check if a file has been uploaded
# if file1_name is not None:
#     # Read the CSV into a DataFrame
#     file1 = pd.read_csv(file1_name)

#     # Display the DataFrame
#     screen1.subheader("Here is your first uploaded file:")
#     screen2.dataframe(file1)  # Streamlit interactive table

#     message_screen.write("Now scroll down and select a csv file to merge with the one you just selected.")


#     if file1_name is not None:
#         # File2 uploader
#         file2_name = screen3.file_uploader("Choose the CSV file to be merged with the first file", type=["csv"])

#         # Check if a file has been uploaded
#         if file2_name is not None:
#             # Read the CSV into a DataFrame
#             file2 = pd.read_csv(file2_name)

#             # Display the DataFrame
#             screen3.subheader("Here is your second uploaded file:")
#             screen4.dataframe(file2)  # Streamlit interactive table

#         if file2_name is not None:

            # screen5.subheader("Merged (Joined) File")
            # result = pd.concat([file1, file2])
            # screen6.dataframe(result)

            # duplicates = result[result.duplicated(keep=False)]

            # if not duplicates.empty:
            #     screen5.header("The following entries are duplicates. Correct this and try again.")
            #     screen6.dataframe(duplicates)

            
#             st.markdown("___")

#             left, right = st.columns(2)

#             if left.button("Click here to merge another file"):
#                 left.markdown("You clicked the plain button.")
            
            
#             if right.button("Click here to save the merged file to your computer"):
#                 right.markdown("You clicked the Material button.")

#             @st.cache_data
#             def save_result(result):  
#                 return result.to_csv().encode("utf-8")
            

#             csv = save_result(result)

#             filename = st.text_input("Enter filename for CSV (including .csv)")

#             st.download_button(
#                 label=':floppy_disk: Click here to save your data on your local computer',
#                 data=csv,
#                 file_name=filename,
#                 mime="text/csv",
#             )

#     else:
#         message_screen.info("Now upload the CSV file to be merged with the first.")

# else:
#     message_screen.info("Please upload a CSV file in the box below.")
