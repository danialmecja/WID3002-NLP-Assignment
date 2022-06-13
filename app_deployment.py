import streamlit as st
import pandas as pd
import numpy as np
# Page style

# Functions 
def get_reviews_facility(facility):
    if len(facility) != 0:
        facility_name = facility[0]
        st.write('The facility you have chosen is ', facility_name)
        facility_data = data[data['name'].str.contains(facility_name)]
        #st.table(facility_data)
        st.write('Location: ',facility_data['locality'].iloc[0])
        facility_service = facility_data['overall_service_score'].iloc[0]
        display_ratings('Service:',facility_service)
        facility_facilities = facility_data['overall_facility_score'].iloc[0]
        display_ratings('Facilities:',facility_facilities)
        facility_cost = facility_data['overall_cost_score'].iloc[0]
        display_ratings('Cost:',facility_cost)

def get_reviews_locality(locality):
    facility = locality
    if len(facility) != 0:
        facility_name = facility[0]
        st.write('The facility you have chosen is ', facility_name)
        facility_data = data[data['locality'].str.contains(facility_name)]
        st.table(facility_data)
        st.write('Location: ',facility_data['locality'].iloc[0])
        facility_service = facility_data['overall_service_score'].iloc[0]
        display_ratings('Service:',facility_service)
        facility_facilities = facility_data['overall_facility_score'].iloc[0]
        display_ratings('Facilities:',facility_facilities)
        facility_cost = facility_data['overall_cost_score'].iloc[0]
        display_ratings('Cost:',facility_cost)

def display_ratings(category, rating):
    st.write(category,":")
    if rating == 5:
        st.markdown(":star::star::star::star::star:")
    elif rating >=4 and rating <5:
        st.markdown(":star::star::star::star:")
    elif rating >=3 and rating <4:
        st.markdown(":star::star::star:")
    elif rating >=2 and rating <3:
        st.markdown(":star::star:")
    else:
            st.markdown(":star:")
# Page starts here
st.title('AMITY - Review Management with Sentiment Analysis')
st.image('images\header.jpg')
overall_category = ('Overall_Category_Score.csv')
data = pd.read_csv(overall_category)



st.header('Find the healthcare you need!')
search_radio = st.radio('Find healthcare facility by:', ['direct facility', 'current location'])
if search_radio == 'direct facility':
    facility = st.multiselect('Enter name of facility',data['name'])
    get_reviews_facility(facility)
elif search_radio == 'current location' :
    locality = st.multiselect('Enter location',data['locality'].unique())
    get_reviews_locality(locality)

    




##User journey 1 -> user input = Facility name
