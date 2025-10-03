import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide",page_title="Startup Analysis")

df=pd.read_csv("startup_cleaned.csv")
df['Date'] = pd.to_datetime(df['Date'],errors='coerce')
df['Year'] = df['Date'].dt.year
df["Months"] = df["Date"].dt.month
df["Months"] = pd.to_datetime(df["Months"],errors="coerce").astype(int)



def load_overall_analysis():
    st.title("Overall Analysis")
    col1, col2, col3,col4 = st.columns(4)
    with col1:
        #Toatal Amount Invested
        total=df["Amount"].sum()
        st.metric("Total Amount", str(round(total)) + "Cr")
    with col2:
        #Maximum Amount infused in a startup
        max_fund=df.groupby("Stratup")["Amount"].max().sort_values(ascending=False).head(1).values[0]
        st.metric("Max Amount", str(round(max_fund)) + "Cr")
    #Average Funding to Startups
    with col3:
        avg=df.groupby("Stratup")["Amount"].sum().mean()
        st.metric("Avg Amount", str(round(avg)) + "Cr")
    #Total funded startups
    with col4:
        funded=df["Stratup"].nunique()
        st.metric("Total Funded startups", str(round(funded)))

    #MOM investment Graph
    st.header("Mom graph")
    temp = df.groupby(["Year", "Months"])["Amount"].sum().reset_index()
    temp["x_axix"] = temp['Months'].astype("str") + " " + temp['Year'].astype("str")
    fig3, ax3 = plt.subplots()
    ax3.plot(temp["x_axix"],temp["Amount"])
    st.pyplot(fig3)
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


    # year_series = df[df['Investors Name'].str.contains(investor)].groupby('Year')['Amount'].sum()
    #
    # st.subheader('YoY Investment')
    # fig2, ax2 = plt.subplots()
    # ax2.plot(year_series.index,year_series.values)
    #
    # st.pyplot(fig2)


st.sidebar.title("Startup Funding Analysis")

option=st.sidebar.selectbox("Select one",["Overall Analysis","Startup","Investor"])

if option=="Overall Analysis":
    btn0=st.sidebar.button("Show Overall Analysis")
    if btn0:
        load_overall_analysis()

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
