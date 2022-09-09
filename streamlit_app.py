import streamlit as st
# packages for connecting to postgres
import psycopg2
import pandas as pd
from plotly import graph_objects as go


DATABASE_URL = st.secrets["database_url"]
TABLE_NAME = 'aielabs_aielabsapplicationform'

# connect to database
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()

# display schema
if False:
    cur.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{TABLE_NAME}'")
    schema = cur.fetchall()
    st.write(schema)
    print(schema)

# schema:
# [('firstName', 'text'), ('lastName', 'text'), ('email', 'character varying'), ('phoneNumber', 'text'), ('dateOfBirth', 'date'), ('nationality', 'text'), ('placeOfResidence', 'text'), ('linkedin', 'text'), ('website', 'text'), ('github', 'text'), ('pursuingDegree', 'text'), ('university', 'text'), ('participationReason', 'text'), ('whatToLearn', 'text'), ('areasOfInterest', 'text'), ('skills', 'text'), ('programmingExperience', 'text'), ('partOfTeam', 'boolean'), ('idea', 'text'), ('heardAbout', 'text'), ('participationConfirmation', 'boolean'), ('createdAt', 'timestamp with time zone'), ('id', 'integer')]


# get data from database
cur.execute(f"SELECT * FROM {TABLE_NAME}")
rows = cur.fetchall()
df = pd.DataFrame(rows)
df.columns = [desc[0] for desc in cur.description]


# filter the data
# remove all entries where the first name starts with 'test'
df = df[~df['firstName'].str.startswith('test')]

# remove all entries where the first name is 'Can' and the last name is 'Kayalan'
df = df[~((df['firstName'] == 'Can') & (df['lastName'] == 'Kayalan'))]


# creaete a graph of the cumulative number of applications over time
st.subheader('Cumulative applications over time')
created_at = df['createdAt'].value_counts().sort_index()
fig = go.Figure()
fig.add_trace(go.Scatter(x=created_at.index, y=created_at.cumsum()))
st.plotly_chart(fig, use_container_width=True)

# age distribution
st.subheader('Age distribution')
age = df['dateOfBirth'].apply(lambda x: 2021 - x.year)
age = age.value_counts().sort_index()
fig = go.Figure()
fig.add_trace(go.Bar(x=age.index, y=age.values))
st.plotly_chart(fig, use_container_width=True)

# nationality distribution
st.subheader('Nationality distribution')
nationality = df['nationality'].value_counts().sort_values(ascending=False)
fig = go.Figure()
fig.add_trace(go.Bar(x=nationality.index, y=nationality.values))
st.plotly_chart(fig, use_container_width=True)

# place of residence distribution
st.subheader('Place of residence distribution')
place_of_residence = df['placeOfResidence'].value_counts().sort_values(ascending=False)
place_of_residence.index = place_of_residence.index.str.strip()
fig = go.Figure()
fig.add_trace(go.Bar(x=place_of_residence.index, y=place_of_residence.values))
st.plotly_chart(fig, use_container_width=True)

# pursuing degree distribution
st.subheader('Pursuing degree distribution')
pursuing_degree = df['pursuingDegree'].value_counts().sort_values(ascending=False)
fig = go.Figure()
fig.add_trace(go.Bar(x=pursuing_degree.index, y=pursuing_degree.values))
st.plotly_chart(fig, use_container_width=True)

# university distribution
st.subheader('University distribution')
university = df['university'].value_counts().sort_values(ascending=False)
fig = go.Figure()
fig.add_trace(go.Bar(x=university.index, y=university.values))
st.plotly_chart(fig, use_container_width=True)

# part of team distribution
st.subheader('Part of team distribution')
part_of_team = df['partOfTeam'].value_counts().sort_values(ascending=False)
fig = go.Figure()
fig.add_trace(go.Bar(x=part_of_team.index, y=part_of_team.values))
st.plotly_chart(fig, use_container_width=True)



