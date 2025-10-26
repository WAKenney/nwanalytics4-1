import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import streamlit as st

#Create page title
titleCol1, titleCol2, titleCol3 =st.columns((1,4,1))

title = 'new_nw_header.png'

titleCol2.image(title, use_container_width=True)

st.subheader('Tree Ownership Analysis')

st.markdown("___")

screen1 = st.empty()
screen2 = st.empty()
screen3 = st.empty()

st.markdown("___")


def ownership(data):
    """Analyze tree ownership - City, Provate or Jointly owned"""

    data = data.loc[data['diversity_level'] != 'other']

    ownershipText = {'c':'City', 'p':'Private', 'j':'Joint'}
    data['ownership_code'] = data['ownership_code'].map(ownershipText)

    with st.expander("Click here to read an explanation of Ownership summary.", expanded=False):
        
            st.markdown('''Coming soon ..... 
                '''
            )
    
        # By frequency

    st.subheader("Ownership by the number of trees (frequency)")

    ownershipData = data.loc[: , ['ownership_code', 'tree_name']]

    # ownershipData.fillna('not assessed')

    ownershipPT = pd.pivot_table(ownershipData, index='ownership_code', aggfunc='count')
    ownershipPT.reset_index(inplace=True)
    
    ownershipPT.rename(columns = {'tree_name': 'frequency'},inplace = True)


    ownershipPie = px.pie(ownershipPT, values='frequency', names = 'ownership_code')
    
    ownershipPie.update_traces(insidetextorientation='radial', textinfo='label+percent') 
    ownershipPie.update_layout(showlegend=False)
    ownershipPie.update_traces(textfont_size=15,
                  marker=dict(line=dict(color='#000000', width=1)))
    
    st.plotly_chart(ownershipPie)

    # By CPA

    st.subheader("Ownership by crown projection area (cpa)")

    ownershipDataCPA = data.loc[: , ['ownership_code', 'cpa']]

    ownershipPTCPA = pd.pivot_table(ownershipDataCPA, index='ownership_code', aggfunc='sum')
       
    ownershipPTCPA.reset_index(inplace=True)
    
    # ownershipPTCPA.rename(columns = {'ownership' : 'Ownership'},inplace = True)
    
    ownershipPieCPA = px.pie(ownershipPTCPA, values='cpa', names = 'ownership_code')
    
    ownershipPieCPA.update_traces(insidetextorientation='radial', textinfo='label+percent') 
    ownershipPieCPA.update_layout(showlegend=False)
    ownershipPieCPA.update_traces(textfont_size=15,
                  marker=dict(line=dict(color='#000000', width=1)))
    
    st.plotly_chart(ownershipPieCPA)


if len(st.session_state['df_trees']) == 0:

    screen2.error("You haven't loaded a file yet.  Either go to the 'Create or Refresh...' function in the side bar or the ' Load an Existing...")

else:

    ownership(st.session_state.select_df)
    
    if st.session_state['total_tree_count'] != st.session_state['select_tree_count']:

        screen1.markdown(f"#### There are :red[{st.session_state['select_tree_count']}] entries in the filtered data. ")

    else:

        screen1.markdown(f"#### All :red[{st.session_state['total_tree_count']}] entries are shown (no filter). ")

