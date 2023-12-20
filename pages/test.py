import streamlit as st
import pandas as pandas

df=st.session_state.df_trees
st.dataframe(df, hide_index=True, use_container_width=True,
             column_config = {
                 "tree_name":"Tree Name", 'use_container_width':'True',
                 "cpa":st.column_config.NumberColumn("Crown Projection Area (m2)", format = "%.0f")

                 

             }
             
             )