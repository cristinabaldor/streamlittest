
import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
import json
import requests
import csv
# import geopandas
import folium
from streamlit_folium import folium_static
# from bokeh.plotting import figure
# from bokeh.io import show
from matplotlib import pyplot as plt
# import pandas_bokeh


st.title("Healthy Districts")

st.write("This is outside the container")


health_df = pd.read_csv("district_data.csv")
# The LCL and UCL columns represent the lower- and upper- confidence levels for the metrics.
# Here those columns are removed.
health_data_reduced = health_df.drop(columns=['lackinsurance_LCL',
                                              'lackinsurance_UCL',
                                              'chekup_LCL',
                                              'checkup_UCL',
                                              'cholscreen_LCL',
                                              'cholscreen_UCL',
                                              'diabetes_LCL',
                                              'diabetes_UCL',
                                              'flushot_LCL',
                                              'flushot_UCL',
                                              'ghlth_LCL', 'ghlth_UCL',
                                              'physical_inactivity_LCL',
                                              'physical_inactivity_UCL',
                                              'physical_inactivity_LCL',
                                              'physical_inactivity_UCL',
                                              'mcost_LCL',
                                              'mcost_UCL',
                                              'mhlth_LCL',
                                              'mhlth_UCL',
                                              'obesity_LCL',
                                              'obesity_UCL',
                                              'csmoking_LCL',
                                              'csmoking_UCL',
                                              ])
# Renaming C116 to GEOID column for matching with other data
health_df = health_data_reduced.rename(columns={'CD116': "GEOID",
                                                'State-District': 'state_district'
                                                })

health_df['GEOID'] = health_df['GEOID'].astype(str).str.zfill(4)

# Converting percentages from strings to floats
health_df['lackinsurance'] = health_df['lackinsurance'].str.strip(
    '%').astype('float')/100.0
health_df['checkup'] = health_df['checkup'].str.strip(
    '%').astype('float')/100.0
health_df['cholscreen'] = health_df['cholscreen'].str.strip(
    '%').astype('float')/100.0
health_df['csmoking'] = health_df['csmoking'].str.strip(
    '%').astype('float')/100.0
health_df['diabetes'] = health_df['diabetes'].str.strip(
    '%').astype('float')/100.0
health_df['flushot'] = health_df['flushot'].str.strip(
    '%').astype('float')/100.0
health_df['ghlth'] = health_df['ghlth'].str.strip('%').astype('float')/100.0
health_df['physical_inactivity'] = health_df['physical_inactivity'].str.strip(
    '%').astype('float')/100.0
health_df['mcost'] = health_df['mcost'].str.strip('%').astype('float')/100.0
health_df['mhlth'] = health_df['mhlth'].str.strip('%').astype('float')/100.0
health_df['obesity'] = health_df['obesity'].str.strip(
    '%').astype('float')/100.0


acsurl = "https://api.census.gov/data/2018/acs/acs1?get=NAME,B01001_001E,B02001_002E,B02001_003E,B02001_004E,B02001_005E,B02001_006E,B02001_007E,B02001_008E,B03003_003E,B29001_001E,B19013_001E,B19301_001E,B25077_001E,B25064_001E,B19083_001E,B25001_001E,B25002_002E,B25003_002E,B25003_003E,B25002_003E&for=congressional%20district:*"

# Requesting API data in JSON format, setting first row imported as headers for dataframe
acs_response = requests.get(f"{acsurl}").json()
acs_df = pd.DataFrame(acs_response)
acs_df.columns = acs_df.iloc[0]
acs_df = acs_df[1:]


# Converting codes to population types, guide here: http://proximityone.com/cd.htm

acs_df = acs_df.rename(columns={"B01001_001E": "totalpop",
                                "B02001_002E": "white",
                                "B02001_003E": "black",
                                "B02001_004E": "amerindian_native",
                                "B02001_005E": "asian",
                                "B02001_006E": "hawaiian_pacific",
                                "B02001_007E": "other_race",
                                "B02001_008E": "two_more_races",
                                "B03003_003E": "hispanic_latino",
                                "B29001_001E": "citizen_voters",
                                "B19013_001E": "median_household_income",
                                "B19301_001E": "per_capita_income",
                                "B25077_001E": "median_housing_value",
                                "B25064_001E": "median_gross_rent",
                                "B19083_001E": "gini_index_of_income_inequality",
                                "B25001_001E": "total_housing_units",
                                "B25002_002E": "occupied_units",
                                "B25003_002E": "owner_occupied_units",
                                "B25003_003E": "renter_occupied_units",
                                "B25002_003E": "vacant_units",
                                "state": "state",
                                "congressional district": "district"})
# Adding a GEOID Column concatenating State and District Codes to get GEOID, which will be Primary Key in database
acs_df["GEOID"] = acs_df["state"] + acs_df["district"]

# Converting to percentages for demographic information
acs_df['totalpop'] = acs_df['totalpop'].astype('float')
acs_df['median_household_income'] = acs_df['median_household_income'].astype(
    'float')
acs_df['white'] = acs_df['white'].astype('float')
acs_df['black'] = acs_df['black'].astype('float')
acs_df['asian'] = acs_df['asian'].astype('float')
acs_df['amerindian_native'] = acs_df['amerindian_native'].astype('float')
acs_df['hawaiian_pacific'] = acs_df['hawaiian_pacific'].astype('float')
acs_df['other_race'] = acs_df['other_race'].astype('float')
acs_df['two_more_races'] = acs_df['two_more_races'].astype('float')
acs_df['hispanic_latino'] = acs_df['hispanic_latino'].astype('float')
acs_df['citizen_voters'] = acs_df['citizen_voters'].astype('float')
acs_df['white_p'] = acs_df['white']/acs_df['totalpop']
acs_df['black_p'] = acs_df['black']/acs_df['totalpop']
acs_df['amerindian_native_p'] = acs_df['amerindian_native']/acs_df['totalpop']
acs_df['asian_p'] = acs_df['asian']/acs_df['totalpop']
acs_df['hawaiian_pacific_p'] = acs_df['hawaiian_pacific']/acs_df['totalpop']
acs_df['other_race_p'] = acs_df['other_race']/acs_df['totalpop']
acs_df['two_more_races_p'] = acs_df['two_more_races']/acs_df['totalpop']
acs_df['hispanic_latino_p'] = acs_df['hispanic_latino']/acs_df['totalpop']
acs_df['citizen_voters_p'] = acs_df['citizen_voters']/acs_df['totalpop']


# Requesting current updated congressional data
# from https://github.com/unitedstates/congress-legislators

congressurl = "https://theunitedstates.io/congress-legislators/legislators-current.csv"
congress_response = requests.get(
    f"{congressurl}", stream=True).content.decode('utf-8')
cr = csv.reader(congress_response.splitlines(), delimiter=',')
my_list = list(cr)
congress_df = pd.DataFrame(my_list[1:], columns=my_list[0])
congress_df['district'] = congress_df['district'].astype(str).str.zfill(2)
# stripping extra spaces from State abbreviations
congress_df.state = congress_df.state.str.strip()

# Get indexes where type column is sen (Senators)
indexNames = congress_df[congress_df['type'] == 'sen'].index

# Delete these row indexes from dataFrame
congress_df.drop(indexNames, inplace=True)


# Getting State FIPS Codes with State Numbers to go with State Abbreviations in Congress file
fips = pd.read_csv('us-state-ansi-fips.csv')
fips = fips.rename(columns={"stname": "name",
                            " st": "number",
                            " stusps": "state"})
fips['number'] = fips['number'].astype(str).str.zfill(2)
# Stripping extra spaces from state abbreviations that were preventing a merge
fips.state = fips.state.str.strip()

# Merging on 'state' to get state numbers into congress dataframe results in NaN
congress_df = congress_df.merge(fips, on='state', how='inner')
# Adding GEOID column
congress_df["GEOID"] = congress_df["number"] + congress_df["district"]

health_acs_merge = pd.merge(acs_df, health_df, on='GEOID')

health_acs_congress_merge = pd.merge(health_acs_merge, congress_df, on="GEOID")

healthy_districts_df = health_acs_congress_merge[['GEOID',
                                                  'totalpop',
                                                  'party',
                                                  'full_name',
                                                  'gini_index_of_income_inequality',
                                                  'median_household_income',
                                                  'white',
                                                  'black',
                                                  'amerindian_native',
                                                  'asian',
                                                  'hawaiian_pacific',
                                                  'other_race',
                                                  'two_more_races',
                                                  'hispanic_latino',
                                                  'citizen_voters',
                                                  'state_district',
                                                  'lackinsurance',
                                                  'csmoking',
                                                  'diabetes',
                                                  'obesity',
                                                  'ghlth',
                                                  'mhlth',
                                                  'url',
                                                  'twitter'
                                                  ]]


table_data_df = healthy_districts_df[['state_district',
                                      'full_name',
                                      'party',
                                      'median_household_income',
                                      'amerindian_native',
                                      'asian',
                                      'black',
                                      'white',
                                      'hispanic_latino',
                                      'lackinsurance',
                                      'csmoking',
                                      'diabetes',
                                      'obesity']]

table_data_df = table_data_df.rename(columns={'state_district': 'District',
                                              'full_name': 'Representative',
                                              'party': 'Political Party',
                                              'median_household_income': 'Median Income',
                                              'amerindian_native': 'American Indian/Alaskan Native',
                                              'asian': 'Asian',
                                              'black': 'Black',
                                              'white': 'White',
                                              'hispanic_latino': "Hispanic/Latino All Races",
                                              'lackinsurance': 'Uninsured',
                                              'csmoking': 'Currently Smoking',
                                              'diabetes': 'Adult Diabetics',
                                              'obesity': 'Obesity'},
                                     )
healthy_districts_df.to_csv("all_data.csv")


data_all = pd.read_csv('all_data.csv')
data_geo = json.load(open('healthy_districts.geojson'))

# def center():
#    address = 'Chicago, USA'
#    geolocator = Nominatim(user_agent="id_explorer")
#    location = geolocator.geocode(address)
#    latitude = location.latitude
#    longitude = location.longitude
#    return latitude, longitude

# for changing type of the maps
# add_select = st.sidebar.selectbox("What data do you want to see?",("Open Street Map"))#for calling the function for getting center of maps
map_sby = folium.Map(tiles="Open Street Map", location=[37, -90], zoom_start=5)  # design for the app
st.title('Map of USA Congressional Districts')
folium_static(map_sby)

st.dataframe(table_data_df)

# Adding selection for different data

dicts = {"totalpop": 'Total Population',
         "gini_index_of_income_inequality": 'Income Inequality',
         "median_household_income": 'Median Income',
         "lackinsurance": 'Uninsured'}

select_data = st.sidebar.radio("totalpop", "gini_index_of_income_inequality", "median_household_income", "lackinsurance")


def threshold(data):
    threshold_scale = np.linspace(data_all[dicts[data]].min(),
                                  data_all[dicts[data]].max(),
                                  10, dtype=float)
  # change the numpy array to a list
    threshold_scale = threshold_scale.tolist()
    threshold_scale[-1] = threshold_scale[-1]
    return threshold_scale


def show_maps(data, threshold_scale):
    maps = folium.Choropleth(geo_data=data_geo,
                         data=data_all,
                         columns=['GEOID', dicts[data]],
                         key_on='feature.properties.GEOID',
                         threshold_scale=threshold_scale,
                         fill_color='YlOrRd',
                         fill_opacity=0.7,
                         line_opacity=0.2,
                         legend_name=dicts[data],
                         highlight=True,
                         reset=True).add_to(map_sby)

folium_static(map_sby)

show_maps(select_data, threshold(select_data))

# Create scatter plots
with st.beta_container():
    st.write("This is inside the container")

    # You can call any Streamlit command, including custom components:
    st.bar_chart(np.random.randn(50, 3))

col1, col2 = st.beta_columns([3, 1])
data = np.random.randn(10, 1)

col1.subheader("A wide column with a chart")
col1.line_chart(data)

col2.subheader("A narrow column with the data")
col2.write(data)

st.balloons()
