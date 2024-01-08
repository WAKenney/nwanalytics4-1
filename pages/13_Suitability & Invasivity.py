import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import streamlit as st

#Create page title
titleCol1, titleCol2, titleCol3 =st.columns((1,4,1))

title = 'new_nw_header.png'

titleCol2.image(title, use_column_width=True)

st.subheader('Tree Species Suitability & Invasivity Analysis')

st.markdown("___")

screen1 = st.empty()

screen2 = st.empty()

screen3 = st.empty()

st.markdown("___")

def speciesSuitablity(data):
    """Summarize species suitability"""

    with st.expander("Click here to read about species suitability", expanded=False):
    
        st.markdown('''Tree species suitability is based on an expert opinion survey conducted by ISA Ontario during the development of
        the Supplement to the Council of Tree and Landscape Appraiser's Guide to tree appraisal 10 edition.  The survey asked experts across Ontario 
        to rate a list of commonly planted species on a series of criteria.  Each species was given a numerical score.  We converted these scores to categories of
        Very Poor (score < 0.5), Poor (0.51 < 0.6), Good (0.61 to 0.7 and Excellent (>0.70)).  Unfortunately, the scoring process carried out by the expert
        panel did NOT include the tendency for a species to be invasive.  We adapted our ranking so that any species considered to be invasive in Ontario 
        would be considered to have a suitability of Very Poor.  See the section below for more details on invasivity. ''')
    
    st.subheader('Suitability by number of trees (frequency)')

    data = data.loc[data['diversity_level'] != 'other']

    suitabilityData = data.loc[: , ['suitability', 'tree_name']]
    
    suitabilityPT = pd.pivot_table(suitabilityData, index='suitability', aggfunc='count')
    
    suitabilityPT.reset_index(inplace=True)
    
    suitabilityPT.rename(columns = {'tree_name': 'frequency'},inplace = True)

    suitabilityPie = px.pie(suitabilityPT, values='frequency', names = 'suitability',
        color = 'suitability',
        color_discrete_map={'Excellent':'darkgreen',
                                'Good':'springgreen',
                                'Poor':'palegreen',
                                'Very Poor':'yellow'})
    
    suitabilityPie.update_traces(insidetextorientation='radial', textinfo='label+percent') 
    
    suitabilityPie.update_layout(showlegend=False)
    
    suitabilityPie.update_traces(textfont_size=15,
                  marker=dict(line=dict(color='#000000', width=1)))
    
    with st.expander("Click to view tabular data.", expanded=False):
    
        suitabilityTable = ff.create_table(suitabilityPT.round(decimals = 0))
    
        st.plotly_chart(suitabilityTable)
        
    st.plotly_chart(suitabilityPie)


    st.subheader('Suitability by crown projection area (cpa)')

    suitabilityDataCPA = data.loc[: , ['suitability', 'cpa']]
    
    suitabilityPTCPA = pd.pivot_table(suitabilityDataCPA, index='suitability', aggfunc='sum')
    
    suitabilityPTCPA.reset_index(inplace=True)
    
    suitabilityPieCPA = px.pie(suitabilityPTCPA, values='cpa', names = 'suitability',
        color = 'suitability',
        color_discrete_map={'Excellent':'darkgreen',
                                'Good':'springgreen',
                                'Poor':'palegreen',
                                'Very Poor':'yellow'})

    suitabilityPieCPA.update_traces(insidetextorientation='radial', textinfo='label+percent') 
    
    suitabilityPieCPA.update_layout(showlegend=False)
    
    suitabilityPieCPA.update_traces(textfont_size=15,
                  marker=dict(line=dict(color='#000000', width=1)))
    
    st.plotly_chart(suitabilityPieCPA)

    st.markdown("___")
    
    st.header('Tree Species Invasivity Summary (Ontario)')
    
    with st.expander("Click here to read about species invasivity", expanded=False):

        st.markdown('''The tree species indicated as invasive are based on data shown in https://www.ontarioinvasiveplants.ca/invasive-plants/species/''')

    st.subheader('Invasivity by the number of trees (frequency)')

    invasivityData = data.loc[: , ['species', 'invasivity', 'tree_name']]

    invasivityPT = pd.pivot_table(invasivityData, index='invasivity', aggfunc='count')
    
    invasivityPT.reset_index(inplace=True)
    
    invasivityPT.rename(columns = {'tree_name': 'frequency'},inplace = True)
    
    invasivityPie = px.pie(invasivityPT, values='frequency', names = 'invasivity',
        color = 'invasivity',
        color_discrete_map={'invasive':'yellow',
                                'non-invasive':'darkgreen'})
    
    invasivityPie.update_traces(insidetextorientation='radial', textinfo='label+percent') 
    
    invasivityPie.update_layout(showlegend=False)
    
    invasivityPie.update_traces(textfont_size=15,
                  marker=dict(line=dict(color='#000000', width=1)))
    
    with st.expander("Click to view invasive vs. non-invasive summary data.", expanded=False):

        invasivityTable = invasivityPT.drop('species', axis=1, inplace=True)

        invasivityTable = ff.create_table(invasivityPT.round(decimals = 0))
    
        st.plotly_chart(invasivityTable)

    # invasiveSpecies = data.loc[data['invasivity'] == 'invasive', 'species']
    
    with st.expander("Click to view a list of invasive tree species in your data set.", expanded=False):
   
        invasiveSpeciesOnly = invasivityData.loc[invasivityData['invasivity']=='invasive']     
        
        invasiveSpeciesOnly.rename(columns = {'tree_name': 'frequency'},inplace = True)
        
        invasivitySpeciesTable = pd.pivot_table(invasiveSpeciesOnly, index='species', values = 'frequency', aggfunc='count')

        invasivitySpeciesTable = invasivitySpeciesTable.sort_values(by=['frequency'], ascending=False)
    
        invasivitySpeciesTable = invasivitySpeciesTable.loc[lambda invasivitySpeciesTable: invasivitySpeciesTable['frequency'] > 0]


        st.dataframe(invasivitySpeciesTable, column_config = {
            "species":"Species",
            "frequency":st.column_config.NumberColumn("Number of Trees", width = 'medium')
            })

    
    st.plotly_chart(invasivityPie)

    st.subheader('Invasivity by crown projection area (cpa)')

    invasivityDataCPA = data.loc[: , ['invasivity', 'cpa']]
    
    invasivityPTCPA = pd.pivot_table(invasivityDataCPA, index='invasivity', aggfunc='sum')
    
    invasivityPTCPA.reset_index(inplace=True)
    
    invasivityPieCPA = px.pie(invasivityPTCPA, values='cpa', names = 'invasivity',
        color = 'invasivity',
        color_discrete_map={'invasive':'yellow',
                                'non-invasive':'darkgreen'})
    
    invasivityPieCPA.update_traces(insidetextorientation='radial', textinfo='label+percent') 
    
    invasivityPieCPA.update_layout(showlegend=False)
    
    invasivityPieCPA.update_traces(textfont_size=15,
                  marker=dict(line=dict(color='#000000', width=1)))
    

    st.plotly_chart(invasivityPieCPA)

if len(st.session_state['select_df']) == 0:

    screen2.error("You haven't loaded a file yet.  Either go to the 'Create or Refresh...' function in the side bar or the ' Load an Existing...")

else:

    speciesSuitablity(st.session_state.select_df)
    
    if st.session_state['total_tree_count'] != st.session_state['select_tree_count']:

        screen1.markdown(f"#### There are :red[{st.session_state['select_tree_count']}] entries in the filtered data. ")

    else:

        screen1.markdown(f"#### All :red[{st.session_state['total_tree_count']}] entries are shown (no filter). ")