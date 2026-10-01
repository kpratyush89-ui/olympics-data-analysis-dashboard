import streamlit as st
import pandas as pd
import plotly.express as px
import preprocess, helper

st.set_page_config(page_title="Olympics Analysis Dashboard", layout="wide")

# Load data locally from current directory
df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocess.preprocess(df, region_df)

st.sidebar.title("Summer Olympics Analysis")
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis')
)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years, country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)
    
    st.title("Medal Tally")
    st.dataframe(medal_tally, use_container_width=True)

elif user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Editions", editions)
        st.metric("Events", events)
    with col2:
        st.metric("Hosts", cities)
        st.metric("Nations", nations)
    with col3:
        st.metric("Sports", sports)
        st.metric("Athletes", athletes)

    nations_over_time = helper.data_over_time(df, 'region')
    fig = px.line(nations_over_time, x="Edition", y="region", title="Participating Nations Over Time")
    st.plotly_chart(fig, use_container_width=True)