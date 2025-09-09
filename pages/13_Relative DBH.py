import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import streamlit as st

#Create page title
titleCol1, titleCol2, titleCol3 =st.columns((1,4,1))

title = 'new_nw_header.png'

titleCol2.image(title, use_container_width=True)

st.subheader('Tree Relative DBH Analysis')

st.markdown("___")

screen1 = st.empty()
screen2 = st.empty()
screen3 = st.empty()

st.markdown("___")

def relativeDBH(data):
    
    """Summarize Relative DBH"""

    with st.expander("Click here to read some comments about the DBH and Relative DBH analysis.", expanded=False):
    
        st.markdown("""
                    The tree diameter at breat height (DBH) values were placed in four classes for easier comparison.  These classes are as follows: 
                    
            __Class I__ represents all trees with a DBH of 20 cm or less;
            
            __Class II__ all trees with a DBH >20 cm and <39 cm;

            __Class III__ all trees with a DBH >40 cm and <59 cm; and

            __Class IV__ all trees with a DBH 60 cm or more.

            Simply looking at the distribution of DBH fails to tell the whole story since the urban forest is usually
            a mixture of species with large stature at maturity and those of small stature.  RDBH is derived by dividing each tree's DBH by the maximum DBH 
            for that species at maturity. We have derived the latter from the literature, municipal inventories and from our database of well over 150,000 trees collected 
            through Neighbour_woods_ inventories.
            
            __RDBH Class I__ represents all trees with a DBH 25% or less of the maximum DBH for the species (Target 40% );

            __RDBH Class II__ all trees with a DBH >25% or <50% of the maximum DBH for the species (Target 30%);

            __RDBH Class III__ all trees with a DBH >50% or <75% of the maximum DBH for the species (Target 20%); and
                    
            __RDBH Class IV__ all trees with a DBH 75% or more of the maximum DBH for the species (Target 10%).

            NOTE: This only includes trees that were identified to the species level and had a DBH recorded.  Not all species currently have a maximum DBH available.

            Targets are adapted from _Richards, N.A. 1983. Diversity and stability in a street tree population. Urban Ecology 7:159-171_.
        """)
    
    numberNan = data['dbh_class'].isnull().sum()
    
    if numberNan != 0:
        if numberNan == 1:
            st.write('There is 1 entry with no DBH Class recorded.  This will be omitted from this anlysis.')    
        else:
            st.write('There are ' + str(numberNan) + ' entries with no DBH Class recorded.  These will be omitted from this anlysis.')

    data = data.loc[data['diversity_level'] == 'species']

    data.dropna(subset=['dbh'], inplace = True)
    data.dropna(subset=['dbh_class'], inplace = True)
    data.dropna(subset=['rdbh_class'], inplace = True)
   
    dbhData = data.loc[: , ['dbh_class', 'tree_name']]
    
    dbhPT = pd.pivot_table(dbhData, index='dbh_class', aggfunc='count')
    dbhPT.reset_index(inplace=True)
    dbhPT.rename(columns = {'dbh_class': 'DBH Class', 'tree_name': 'Frequency'},inplace = True)

    dbhNumberOfEntries = dbhPT['Frequency'].sum()
    
    dbhPT["Target"] = [dbhNumberOfEntries*0.4, dbhNumberOfEntries*0.3, dbhNumberOfEntries*0.2, dbhNumberOfEntries*0.1]
    
    dbhFig = go.Figure(data=[
        go.Bar(name='Current', x= dbhPT['DBH Class'], y=dbhPT['Frequency']),
        go.Bar(name='Target', x=dbhPT['DBH Class'], y=dbhPT['Target'])])

    dbhFig.update_layout(barmode='group', xaxis=dict(title_text='DBH CLass'), yaxis = dict(title_text='Frequency'))
    
    
    st.header("DBH Class Frequency")

    with st.expander("Click here to show DBH class by Frequency and Target ", expanded=False):
        

        rdbhTable = ff.create_table(dbhPT.round(decimals = 0))
        
        st.plotly_chart(rdbhTable)
    
    st.plotly_chart(dbhFig)

    realtiveDbhData = data.loc[: , ['rdbh_class', 'tree_name']]
    
    relativeDbhPT = pd.pivot_table(realtiveDbhData, index='rdbh_class', aggfunc='count')
    relativeDbhPT.reset_index(inplace=True)
    relativeDbhPT.rename(columns = {'rdbh_class': 'Relative DBH Class', 'tree_name': 'Frequency'},inplace = True)

    relativeDbhPT = relativeDbhPT.head(4)

    numberOfEntries = relativeDbhPT['Frequency'].sum()

    relativeDbhPT["Target"] = [numberOfEntries*0.4, numberOfEntries*0.3, numberOfEntries*0.2, numberOfEntries*0.1]

    rdbhFig = go.Figure(data=[
        go.Bar(name='Current', x= relativeDbhPT['Relative DBH Class'], y=relativeDbhPT['Frequency']),
        go.Bar(name='Target', x=relativeDbhPT['Relative DBH Class'], y=relativeDbhPT['Target'])])

    rdbhFig.update_layout(barmode='group', xaxis=dict(title_text='Relative DBH CLass'), yaxis = dict(title_text='Frequency'))
    
    st.header("Relative DBH Class Frequency")

    st.plotly_chart(rdbhFig)


if len(st.session_state['select_df']) == 0:

    screen2.error("You haven't loaded a file yet.  Either go to the 'Create or Refresh...' function in the side bar or the ' Load an Existing...")

else:

    relativeDBH(st.session_state.select_df)
    
    if st.session_state['total_tree_count'] != st.session_state['select_tree_count']:

        screen1.markdown(f"#### There are :red[{st.session_state['select_tree_count']}] entries in the filtered data. ")

    else:

        screen1.markdown(f"#### All :red[{st.session_state['total_tree_count']}] entries are shown (no filter). ")

