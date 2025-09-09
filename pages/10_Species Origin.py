import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import streamlit as st

#Create page title
titleCol1, titleCol2, titleCol3 =st.columns((1,4,1))

title = 'new_nw_header.png'

titleCol2.image(title, use_container_width=True)

st.subheader('Tree Species Origin Analysis')

st.markdown("___")

screen1 = st.empty()
screen2 = st.empty()
screen3 = st.empty()

st.markdown("___")


def speciesOrigin(data):
    """Analyze speecies origin i.e.native vs non-native"""
        
    data = data.loc[data['diversity_level'] != 'other']

   
    with st.expander("Click here to read an explanation of the Species Origin figure.", expanded=False):
        
            st.markdown('''These figures show the proportion of the trees that are native to your region versus those 
                that have been introduced from outside the region.  This is based a series of maps documented in 
                the "Atlas of United States Trees" by Elbert L. Little, Jr.
                Digital versions of the maps for tree species that naturally occur in Ontario (according to Little) 
                were downloaded.  These maps were overlaid (in a GIS) on digital maps of the Ecoregions of Ontario.  
                Any species for which the map overlaid any given Ecoregion by more than 5% of the area of the Ecoregion 
                was considered to be "native" to that Ecoregion. Otherwise, the species was considered to be introduced.
                This approach is much more precise than simply stating if the species is native to Ontario, as is often done. [More information about Little's maps can be found here ](https://web.archive.org/web/20170127093428/https://gec.cr.usgs.gov/data/little/)
                and [the Ecoregions map can be viewed here ](https://geohub.lio.gov.on.ca/datasets/ecoregion/explore?location=42.987702%2C-66.706064%2C8.53)
                
                '''
            )
    
    st.write('Remember, the species origin analysis will NOT include any trees identified only at the genus level (e.g. pinspp, mapspp,  etc.)')

    st.subheader("Origin by the number of trees (frequency)")

    originData = data.loc[: , ['origin', 'tree_name']]

    originData.fillna('not assessed')

    originPT = pd.pivot_table(originData, index='origin', aggfunc='count')
    originPT.reset_index(inplace=True)
    
    originPT.rename(columns = {'seRegion' : 'origin' , 'tree_name': 'frequency'},inplace = True)


    originPie = px.pie(originPT, values='frequency', names = 'origin')
    
    originPie.update_traces(insidetextorientation='radial', textinfo='label+percent') 
    originPie.update_layout(showlegend=False)
    originPie.update_traces(textfont_size=15,
                  marker=dict(line=dict(color='#000000', width=1)))
    
    st.plotly_chart(originPie)

    # By CPA

    st.subheader("Origin by crown projection area (cpa)")

    originDataCPA = data.loc[: , ['origin', 'cpa']]

    originPTCPA = pd.pivot_table(originDataCPA, index='origin', aggfunc='sum')
       
    originPTCPA.reset_index(inplace=True)
    
    originPTCPA.rename(columns = {'seRegion' : 'origin'},inplace = True)
    
    originPieCPA = px.pie(originPTCPA, values='cpa', names = 'origin')
    
    originPieCPA.update_traces(insidetextorientation='radial', textinfo='label+percent') 
    originPieCPA.update_layout(showlegend=False)
    originPieCPA.update_traces(textfont_size=15,
                  marker=dict(line=dict(color='#000000', width=1)))
    
    st.plotly_chart(originPieCPA)



if len(st.session_state['df_trees']) == 0:

    screen2.error("You haven't loaded a file yet.  Either go to the 'Create or Refresh...' function in the side bar or the ' Load an Existing...")

else:

    speciesOrigin(st.session_state.select_df)
    
    if st.session_state['total_tree_count'] != st.session_state['select_tree_count']:

        screen1.markdown(f"#### There are :red[{st.session_state['select_tree_count']}] entries in the filtered data. ")

    else:

        screen1.markdown(f"#### All :red[{st.session_state['total_tree_count']}] entries are shown (no filter). ")

