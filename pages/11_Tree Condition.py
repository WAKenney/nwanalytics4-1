import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import streamlit as st

#Create page title
titleCol1, titleCol2, titleCol3 =st.columns((1,4,1))

title = 'new_nw_header.png'

titleCol2.image(title, use_column_width=True)

# st.subheader('Tree Species Origin Analysis')

st.markdown("___")

screen1 = st.empty()

st.markdown("___")

screen2 = st.empty()
screen3 = st.empty()

st.markdown("___")

screen1.markdown(f'## Tree Condition Analysis')

def treeCondition(data):
    """Summarize tree condition """

    st.markdown("___")
    st.header('Tree Condition Summary')
    
    try:
    
        cols = ['0', '1', '2', '3']

        df = pd.DataFrame(index = condColumns, columns = cols)

        for cond in condColumns:
            
            myValues = pd.to_numeric(data[cond], errors = 'coerce').value_counts(bins = 4)
            
            df.at[cond,'0'] = myValues.iloc[0]
            df.at[cond,'1'] = myValues.iloc[1]
            df.at[cond,'2'] = myValues.iloc[2]
            df.at[cond,'3'] = myValues.iloc[3]

        df.reset_index(inplace=True)
        df = df.rename(columns = {'index':'Condition Attribute'})
        
        with st.expander("Click here to show Data Summary by Condition Attribute and Score", expanded=False):

            condTable = ff.create_table(df)
            st.plotly_chart(condTable)


        conditionData = data.loc[: , ['defects', 'tree_name']]
        conditionPT = pd.pivot_table(conditionData, index='defects', aggfunc='count')
        conditionPT.reset_index(inplace=True)
        
        conditionPT.rename(columns = {'tree_name': 'frequency'},inplace = True)

        conditionPie = px.pie(conditionPT, values='frequency', names = 'defects')
        
        conditionPie.update_traces(insidetextorientation='radial', textinfo='label+percent') 
        conditionPie.update_layout(showlegend=False)
        conditionPie.update_traces(textfont_size=15,
                    marker=dict(line=dict(color='#000000', width=1)))
        
        st.subheader("Condition by the number of trees (frequency)")
        st.plotly_chart(conditionPie)

        conditionDataCPA = data.loc[: , ['defects', 'cpa']]
        conditionPTCPA = pd.pivot_table(conditionDataCPA, index='defects', aggfunc='sum')
        conditionPTCPA.reset_index(inplace=True)
        
        conditionPieCPA = px.pie(conditionPTCPA, values='cpa', names = 'defects')
        
        conditionPieCPA.update_traces(insidetextorientation='radial', textinfo='label+percent') 
        conditionPieCPA.update_layout(showlegend=False)
        conditionPieCPA.update_traces(textfont_size=15,
                    marker=dict(line=dict(color='#000000', width=1)))
        

        st.subheader("Condition by Crown Projection Area (cpa)")
        st.plotly_chart(conditionPieCPA)

    except ValueError:

        st.warning('''Oh oh!  There may be a problem with your data.  Run the "Check Data" function (in the sidebar) 
        and look for errors in the column at the right of the table that is generated.  You can filter the error column
        in the table just as you would in the main table to find everything that isn't "ok".  Correct any errors in your data input file
        then re-start this app, re-load the corrected file and proceed. Only 0, 1, 2 or 3 (0 or 1 for conks) are valid entries in any of the 
        condition columns (reduced_crown to recent_trenching). Any other value, including a blank, in these columns will 
        cause NWAnalytics3 to stop working!''')





if st.session_state['select_df'] is not None:

        if st.session_state['total_tree_count'] != st.session_state['select_tree_count']:

            screen2.markdown(f"#### There are :red[{st.session_state['select_tree_count']}] entries in the filtered data. ")

        else:

            screen2.markdown(f"#### All :red[{st.session_state['total_tree_count']}] entries are shown (no filter). ")
            # st.session_state['df_trees']

        treeCondition(st.session_state.select_df)
