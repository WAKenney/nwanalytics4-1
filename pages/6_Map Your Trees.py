import folium
from folium.plugins import Fullscreen
import streamlit as st
from streamlit_folium import folium_static

#Create page title
titleCol1, titleCol2, titleCol3 =st.columns((1,4,1))

title = 'new_nw_header.png'

titleCol2.image(title, use_column_width=True)

st.subheader('Map Your Trees')

st.markdown("___")

screen1 = st.empty()
screen2 = st.empty()
screen3 = st.empty()

st.markdown("___")

def mapItFolium(mapData):
    '''Generates a folium map using the selected dataframe
    '''
    screen2.markdown(f"#### Setting up the map data.")

    mapData.rename(columns = {'Tree Name' : 'tree_name', 'Longitude' : 'longitude', 'Latitude' : 'latitude', 'Crown Width' : 'crown_width', 
                              'Defect Colour' : 'defectColour', 'Description' : 'description'}, inplace = True)
    
    pointSizeSlider = st.slider('Move the slider to adjust the point size', min_value = 2, max_value = 20, value =4)
        
    # if mapData is None:
    #     st.warning("Be sure to finish selecting the filtering values in the sidebar to the left.")

    # Drop entries with no latitude or longitude values entered
    mapData = mapData[mapData['latitude'].notna()] 
    mapData = mapData[mapData['longitude'].notna()]

    mapData['crown_radius'] = mapData['crown_width']/2

    #calculate the corner points of the data to use to centre the map
    maxLat=mapData['latitude'].max()
    minLat=mapData['latitude'].min()
    maxLon=mapData['longitude'].max()
    minLon=mapData['longitude'].min()
    
    #setup the map
    screen2.markdown(f"#### Preparing the map.")
    treeMap = folium.Map(location=[st.session_state['avLat'], st.session_state['avLon']],  
        zoom_start=5,
        max_zoom=100, 
        min_zoom=1, 
        width ='100%', height = '100%', 
        prefer_canvas=True, 
        control_scale=True,
        tiles='OpenStreetMap'
        )

    treeMap.fit_bounds([[minLat,minLon], [maxLat,maxLon]])

    mapData.apply(lambda mapData:folium.CircleMarker(location=[mapData["latitude"], mapData["longitude"]], 
        color='white', # use a white border on the circle marker so it will show up on satellite image
        stroke = True,
        weight = 1,
        fill = True,
        fill_color=mapData['defectColour'],
        fill_opacity = 0.6,
        line_color='#000000',
        radius= pointSizeSlider, #setup a slide so the use can chage the size of the marker
        tooltip = mapData['tree_name'],
        popup = folium.Popup(mapData["description"], 
        name = "Points",
        max_width=450, 
        min_width=300)).add_to(treeMap), 
        axis=1)

    #have an ESRI satellite image as an optional base map
    folium.TileLayer(
        tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr = 'Esri',
        name = 'Satellite',
        overlay = False,
        control = True
       ).add_to(treeMap)

    # add a fullscreen option and layer control to the map
    Fullscreen().add_to(treeMap)
    
    #add a layer control to the map
    folium.LayerControl().add_to(treeMap)
    
    # Show the map in Streamlit

    screen2.empty()

    folium_static(treeMap)

if len(st.session_state['df_trees']) == 0:

    screen2.error("You haven't loaded a file yet.  Either go to the 'Create or Refresh...' function in the side bar or the ' Load an Existing...")

else:

    mapItFolium(st.session_state['select_df'])

    if st.session_state['total_tree_count'] != st.session_state['select_tree_count']:

        screen1.markdown(f"#### There are :red[{st.session_state['select_tree_count']}] entries in the filtered data. ")

    else:

        screen1.markdown(f"#### All :red[{st.session_state['total_tree_count']}] entries are shown (no filter). ")
        
