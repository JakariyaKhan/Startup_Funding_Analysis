import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide",page_title="Startup Analysis")

df=pd.read_csv("startup_cleaned.csv")

def selected_investor_details(investor):
    st.title(investor)
    #Loading Recent Investings
    last5=df[df['Investors Name'].str.contains(investor)].head()[['Date','Stratup','Vertical','City  Location','Round','Amount']]
    st.subheader("Most Recent Investments Details(Top 5)")
    st.dataframe(last5)
    col1, col2 = st.columns(2)
    with col1:
        #Loading Biggest Investments
        big=df[df['Investors Name'].str.contains(investor)].groupby('Stratup')['Amount'].sum().sort_values(ascending=False).head()
        st.subheader("Biggest Investment")
        # st.dataframe(big)
        fig, ax = plt.subplots()
        ax.bar(big.index, big.values)
        st.pyplot(fig)
    with col2:
        verical_series = df[df['Investors Name'].str.contains(investor)].groupby('Vertical')['Amount'].sum()

        st.subheader('Sectors invested in')
        fig1, ax1 = plt.subplots()
        ax1.pie(verical_series,labels=verical_series.index,autopct="%0.01f%%")

        st.pyplot(fig1)

    df['year'] = df['date'].dt.year
    year_series = df[df['Investors Name'].str.contains(investor)].groupby('year')['Amount'].sum()

    st.subheader('YoY Investment')
    fig2, ax2 = plt.subplots()
    ax2.plot(year_series.index,year_series.values)

    st.pyplot(fig2)


st.sidebar.title("Startup Funding Analysis")

option=st.sidebar.selectbox("Select one",["Overall Analysis","Startup","Investor"])

if option=="Overall Analysis":
    st.title("Overall Analysis")
elif option=="Startup":
    st.sidebar.selectbox("Select Startup",sorted(df["Stratup"].unique().tolist()))
    btn1=st.sidebar.button("Find Startup Details")
    st.title("Startup Analysis")

else:
    selected_investor=st.sidebar.selectbox("Select Investor",sorted(set(df["Investors Name"].str.split(',').sum())))
    btn2=st.sidebar.button("Find Investor Details")
    if btn2:
        selected_investor_details(selected_investor)
    # st.title("Investor Analysis")
