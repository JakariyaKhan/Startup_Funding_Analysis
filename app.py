import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df=pd.read_csv("startup_cleaned.csv")

def selected_investor_details(investor):
    st.title(investor)
    #Loading Recent Investings
    last5=df[df['Investors Name'].str.contains(investor)].head()[['Date','Stratup','Vertical','City  Location','Round','Amount']]
    st.subheader("Most Recent Investments Details(Top 5)")
    st.dataframe(last5)

    #Loading Biggest Investments
    big=df[df['Investors Name'].str.contains(investor)].groupby('Stratup')['Amount'].sum().sort_values(ascending=False).head()
    st.subheader("Biggest Investment")
    fig, ax = plt.subplots()
    ax.bar(big.index, big.values)
    st.pyplot(fig)


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
