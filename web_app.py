#! /usr/bin/env python3
# coding: utf-8

import map as map
import streamlit as st 
from PIL import Image
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("2021Jun23.csv", low_memory=False)
df = df.drop(index = 0, axis=0)
df = df.drop(index = 1, axis=0)
df = df.dropna(how='all', axis=1)
data = df[19750:23600]
data = data.dropna(how='all', axis=1)
data = data[['Lat', 'Lon', 'COG', 'SOG','Trim','Heel', 'Forestay','Leeway', 'TWD', 'TWS', 'TWA', 'AWA','BSP']]
data['VMG'] = abs(np.cos(data['TWA']*np.pi/180)*data['BSP'])

Upwind = data[(abs(data.TWA)<=60)].reset_index()
Downwind = data[(abs(data.TWA)>=100)].reset_index()
Tribord = data[(data.TWA)>0].reset_index()
Babord = data[(data.TWA<=0)].reset_index()

upwind_trib = pd.merge(Upwind, Tribord, how ='inner')
upwind_bab = pd.merge(Upwind, Babord, how ='inner')
downwind_trib = pd.merge(Downwind, Tribord, how ='inner')
downwind_bab = pd.merge(Downwind, Babord, how ='inner')


def main():

    return 


if __name__ == '__main__':
    title_container = st.beta_container()
    col1, col2 = st.beta_columns([4, 20])
    image = Image.open('mathilde.jpg')
    with title_container:
        with col1:
            st.image(image, width=100)
        with col2:
            st.title("Mathilde Porto Cervo race analysis")

    day_number = st.sidebar.selectbox(
        'select day',
        ["day 1", "day 2","day 3", "day 4"]
    )

    race_number = st.sidebar.selectbox(
        'select race number',
         ["1", "2"]
    )

    option = st.selectbox(
        'Scope analysis',
        ["upwind", "downwind", "manoeuvre", "tactic"])
    
    if option == "upwind":
        fig1, ax1 = plt.subplots()
        plt.title("Boat speed upwind")
        ax1.plot(Upwind['BSP'])
        st.pyplot(fig1)
        fig, ax = plt.subplots()
        plt.title('Port vs Starboard')
        ax.plot(upwind_bab['BSP'], label = 'port')
        ax.plot(upwind_trib['BSP'], label = 'starboard')
        plt.legend()
        st.pyplot(fig)

        fig3, ax3 = plt.subplots()
        plt.title("VMG upwind")
        ax3.plot(Upwind['VMG'])
        st.pyplot(fig3)

        fig4, ax4 = plt.subplots()
        plt.title("TWA upwind")
        ax4.plot(abs(Upwind['TWA']))
        st.pyplot(fig4)
        st.write("avergae TWA", abs(Upwind['TWA']).mean())

        figa, axa = plt.subplots()
        plt.title('Port vs Starboard')
        axa.plot(abs(upwind_bab['TWA']), label = 'port')
        axa.plot(abs(upwind_trib['TWA']), label = 'starboard')
        plt.legend()
        st.pyplot(figa)
        st.write("avergae TWA on port", abs(upwind_bab['TWA']).mean(), "avergae TWA on starboard", abs(upwind_trib['TWA']).mean())
        

        fig2, ax2 = plt.subplots()
        plt.title("Leeway vs boat speed")
        ax2.scatter(Upwind['BSP'], abs(Upwind['Leeway']))
        st.pyplot(fig2)
        leeway = abs(Upwind['Leeway']).mean()
        st.write("Average Leeaway : ", leeway)
        st.write("Average Heel : ", abs(Upwind.Heel).mean())
    

    if option == "downwind":
        fig1, ax1 = plt.subplots()
        plt.title("Boat speed Downwind")
        ax1.plot(Downwind['BSP'])
        st.pyplot(fig1)
        fig, ax = plt.subplots()
        plt.title('Port vs Starboard')
        ax.plot(downwind_bab['BSP'], label = 'port')
        ax.plot(downwind_trib['BSP'], label = 'starboard')
        plt.legend()
        st.pyplot(fig)

        fig3, ax3 = plt.subplots()
        plt.title("VMG Downwind")
        ax3.plot(Downwind['VMG'])
        st.pyplot(fig3)

        fig4, ax4 = plt.subplots()
        plt.title("TWA Downwind")
        ax4.plot(abs(Downwind['TWA']))
        st.pyplot(fig4)
        st.write("avergae TWA", abs(Downwind['TWA']).mean())

        figa, axa = plt.subplots()
        plt.title('Port vs Starboard')
        axa.plot(abs(downwind_bab['TWA']), label = 'port')
        axa.plot(abs(downwind_trib['TWA']), label = 'starboard')
        plt.legend()
        st.pyplot(figa)
        st.write("avergae TWA on port", abs(downwind_bab['TWA']).mean(), "avergae TWA on starboard", abs(downwind_trib['TWA']).mean())
        

        fig2, ax2 = plt.subplots()
        plt.title("Leeway vs boat speed")
        ax2.scatter(Downwind['BSP'], abs(Downwind['Leeway']))
        st.pyplot(fig2)
        leeway = abs(Downwind['Leeway']).mean()
        st.write("Average Leeaway : ", leeway)
        st.write("Average Heel : ", abs(Downwind.Heel).mean())


    if option == "manoeuvre":

        tack = []
        for t in range(len(Upwind)-1):
            if (np.sign(Upwind['TWA'].iloc[t]) != np.sign(Upwind['TWA'].iloc[t+1])) == True:
                tack.append(t)
        Tack = Upwind.loc[(tack)]

        gybe = []
        for t in range(len(Downwind)-1):
            if (np.sign(Downwind['TWA'].iloc[t]) != np.sign(Downwind['TWA'].iloc[t+1])) == True:
                gybe.append(t)
        Gybe = Downwind.loc[(gybe)]

        MEAN_tack = pd.DataFrame()
        for t in tack: 
            MEAN_tack[f"{t}"] = Upwind.BSP[t-10 : t+60].reset_index()['BSP']
        MEAN_tack.mean(axis=1).plot()
        
        MEAN_gybe = pd.DataFrame()
        for t in tack: 
            MEAN_gybe[f"{t}"] = Downwind.BSP[t-30 : t+60].reset_index()['BSP']
        MEAN_gybe.mean(axis=1).plot()

        fig, ax = plt.subplots()
        plt.title("Average tack :from 10s before to 60s after")
        ax.plot(MEAN_tack.mean(axis=1))
        st.pyplot(fig)

        fig1, ax1 = plt.subplots()
        plt.title("Average gybe :from 30s before to 60s after")
        ax1.plot(MEAN_gybe.mean(axis=1))
        st.pyplot(fig1)
        


    if option == "tactic":
        damping = int(st.slider("Select a damping ", min_value=1,   
                       max_value=120,value=5, step=1))
        

        fig, ax = plt.subplots()
        plt.title("TWD during the race")
        ax.plot(data.TWD.rolling(window=int(f"{damping}")).mean())
        st.pyplot(fig)

        figA, axA = plt.subplots()
        plt.title("TWD during the race")
        axA.plot(data.TWS.rolling(window=int(f"{damping}")).mean())
        st.pyplot(figA)
        
        
        

        


