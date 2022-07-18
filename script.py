import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

st.title("Canada's Refugee Claims in 2019")

## function to initialize importing data
@st.cache
def initialize_df():
    RPD_data = pd.read_pickle("data/data.pkl")

    countries = RPD_data["Country Persecution"].unique()
    countries = [x for x in countries if type(x)==str] # gets rid of NaN in list of countries
    
    positive_regular = list(map(lambda x: RPD_data.loc[(RPD_data["Country Persecution"]==x) & (RPD_data["Explanation "]=="Positive")].shape[0], countries))
    positive_expedited = list(map(lambda x: RPD_data.loc[(RPD_data["Country Persecution"]==x) & (RPD_data["Explanation "]=="Expedited Positive")].shape[0], countries))
    negative_regular = list(map(lambda x: RPD_data.loc[(RPD_data["Country Persecution"]==x) & (RPD_data["Explanation "]=="Negative")].shape[0], countries))
    negative_NCB = list(map(lambda x: RPD_data.loc[(RPD_data["Country Persecution"]==x) & (RPD_data["Explanation "]=="Neg. No Cred Basis")].shape[0], countries))
    withdrawn = list(map(lambda x: RPD_data.loc[(RPD_data["Country Persecution"]==x) & (RPD_data["Explanation "]=="Withdrawn")].shape[0], countries))
    abandoned = list(map(lambda x: RPD_data.loc[(RPD_data["Country Persecution"]==x) & (RPD_data["Explanation "]=="Abandoned")].shape[0], countries))
    deceased = list(map(lambda x: RPD_data.loc[(RPD_data["Country Persecution"]==x) & (RPD_data["Explanation "]=="Deceased")].shape[0], countries))

    positive_all = [sum(x) for x in zip(positive_regular, positive_expedited)]
    negative_all = [sum(x) for x in zip(negative_regular, negative_NCB)]
    other = [sum(x) for x in zip(withdrawn, abandoned, deceased)]

    source = [countries, positive_all, negative_all, other]
    df = pd.DataFrame(source, index = ['Country', 'positive', 'negative', 'other']).T

    df['total'] = [sum(x) for x in list(zip(df.positive, df.negative, df.other))]

    return df

df = initialize_df()

## Bar Chart
with st.container():

    def make_bar_chart(df_bar):
        return alt.Chart(df_bar).mark_bar().encode(
        x=alt.X('Country', sort=list(df_bar['Country'])),
        y=alt.Y('sum(Count)', axis=alt.Axis(title='Count of Decisions')),
        color=alt.Color('Treatment', sort='ascending', scale=alt.Scale(scheme='set1')),
        order=alt.Order(
            'treatment_index',
            sort='ascending'
        ),
        tooltip=['Country','Treatment','Count']
    ).properties(
        height=500
    ).interactive()

    col1, col2 = st.columns(2)
    df_sorted = df.sort_values('total', ascending=False).drop(columns=['total'])

    with col1:
        country_selection = st.radio("Country Selection", ('All Countries', 'Specific Countries'))

    with col2:
        display_remainder = st.radio("Remaining Countries", ('Aggregate', 'Omit'))
    
    # display all countries
    if country_selection == 'All Countries': 
        top_x = st.slider('How many countries to display?', 0, len(df), 25, help='Number of countries to display')

        df_top_x = df_sorted[:top_x]

        if display_remainder == 'Aggregate' and top_x < len(df):
            df_remainder_aggregate = pd.DataFrame(df.sort_values('total', ascending=False)[top_x:].sum()).T.drop(columns=['total'])
            df_remainder_aggregate.loc[0, 'Country'] = 'Bottom ' + str(len(df)-top_x) + ' Countries'
            df_top_x = pd.concat([df_top_x, df_remainder_aggregate])

        df_top_x_long = df_top_x.melt('Country',  var_name='Treatment', value_name='Count')
        df_top_x_long['treatment_index'] = list(map(lambda x: 1 if x=="positive" else (2 if x=="negative" else 3), df_top_x_long['Treatment']))

        bar = make_bar_chart(df_top_x_long)

    # choose specific countries to display
    else: 
        selected_countries = st.multiselect("Which countries to display?", df['Country'], ['Nigeria', 'Haiti', 'Iran'], help='Specific countries to display')
        to_graph = df_sorted.loc[df_sorted['Country'].isin(selected_countries)]

        if display_remainder == 'Aggregate':
            remainder = pd.concat([to_graph, df_sorted]).drop_duplicates(keep=False)
            # aggregate
            remainder_aggregate = pd.DataFrame(remainder.sum()).T
            remainder_aggregate.loc[0, 'Country'] = 'Remaining ' + str(len(remainder)) + ' Countries'
            # make a long df
            to_graph = pd.concat([to_graph, remainder_aggregate])

        to_graph_long = to_graph.melt('Country', var_name='Treatment', value_name='Count')
        to_graph_long['treatment_index'] = list(map(lambda x: 1 if x=="positive" else (2 if x=="negative" else 3), to_graph_long['Treatment']))

        bar = make_bar_chart(to_graph_long)

    st.altair_chart(bar)

st.write(df)

bar = alt.Chart(df).mark_circle().encode(
    x='positive',
    y='negative'
).project(
    "naturalEarth1"
)

st.altair_chart(bar)