import pandas as pd
# import geopandas as gpd
import streamlit as st
# from datetime import datetime
import requests

st.cache_data.clear()

currentDir = "https://raw.githubusercontent.com/WAKenney/NWAnalytics/master/"

# speciesFile = currentDir + 'NWspecies220522.xlsx'
speciesFile = 'NWspecies220522.xlsx'

#Create page title
titleCol1, titleCol2, titleCol3 =st.columns((1,4,1))

title = 'nw4_splash_page.png'




# # Function to get the last commit date and time
# def get_last_commit_datetime(repo_url):
#     api_url = f"{repo_url}/commits"
#     response = requests.get(api_url)
#     if response.status_code == 200:
#         commit_data = response.json()
#         last_commit_datetime = commit_data[0]['commit']['author']['date']
#         return last_commit_datetime
#     else:
#         return "Error: Unable to fetch commit data"

# # GitHub repository URL
# repo_url = "https://github.com/WAKenney/nwanalytics4-1"

# # Display the last commit date and time
# last_commit_datetime = get_last_commit_datetime(repo_url)
# st.write(f"Last commit date and time: {last_commit_datetime}")





titleCol2.image(title)

with st.expander("Click here for help in getting started.", expanded=False):
    st.markdown(f"""
        __Neighbour*woods*__ is a community-based program to assist community groups in the stewardship of the urban forest in their neighbourhood.
        Using Neighbour*woods* Analytics, you can map and analyze various aspects of the urban forest that will help you develop and implement stewardship strategies.
        
        To get started, select your Neighbour*woods* inventory data for analysis.  This data should be either in a Neighbour*woods* INPUT format or a Neighbour*woods* SUMMARY format.
        The INPUT format is that which you have collected in the field.  It includes all the species and site characteristics, the tree measurements, the tree condition data (e.g. defoliation, reduced crow, etc.)
        the conflicts and the x and y (latitude and longitude) coordinates.  To complete the various analyses available in NWAnalytics, several additional parameters 
        must be generated from the inventory data.  To do this, click on the __Create or Refresh a Summary Worksheet__ tab in the sidebar at the left.  You will be asked to 
        select a worksheet. This can be an Excel worksheet with the INPUT data as described above (the "raw" inventory data) or an existing SUMMARY data worksheet that was 
        generate previously but in which you have made some changes or additions.  In the latter case, you are simply refreshing the existing summary.
                
        When you Create or Refresh as file, you will be given a chance to save the data as a SUMMARY file to be used in the future.

        If you have an existing Summary worksheet which you have created or refreshed and then saved, you can simply load that by clicking on the __Load an Existing Summary Worksheet__ tab at the left.
        This will speed up the loading of data without the need to generate the additional parameters.
                
        Once you have either Created/Refreshed a summary sheet or Loaded an Existing Worksheet, you can proceed with the various analyses shown at the left. You can conduct 
        these analyses on all the data, or you can filter the data for specific queries. For hints on filtering your data, click on the button in the __Filter Your Data__ screen.

        In various places you will have opportunities to click on a box for more information, just as you are reading this text.  
        To close these boxes, simply click on the header button again.

        Click on the following link to read more about Neighbourwoods: http://neighbourwoods.org/')

        For support, contact Andy Kenney at:     a.kenney@utoronto.ca

""")

st.session_state['speciesTable'] = []

st.session_state['colorsTable'] = []

st.session_state['df_trees'] = []

st.session_state['select_df'] = []

st.session_state['select_df'] = []

st.session_state['total_tree_count'] = []

st.session_state['select_tree_count'] = []

st.session_state['avLon'] = []

st.session_state['avLat'] = []


@st.cache_data(show_spinner="Loading the species table, please wait ...")
def getSpeciesTable():
    '''Load the species table from the Neighburwoods repo'''

    speciesTable = pd.read_excel(speciesFile,sheet_name = "species")

    # st.dataframe(speciesTable)

    if "speciesTable" not in st.session_state:

        st.session_state['speciesTable'] = []

    st.session_state['speciesTable'] = speciesTable
    
    return speciesTable


speciesTable = getSpeciesTable()


# get the species specific colour from the species table for each entry and create the coloursTable
colorsTable = pd.read_excel(speciesFile,sheet_name = "colors")

colorsTable.set_index('taxon', inplace = True)

st.session_state['colorsTable'] = colorsTable