# import MetaTrader5 as mt5
# import PythonMetaTrader5 as mt5
import mt5
import pandas as pd
# import pandas_ta as ta
import finta as ta
import streamlit as st




@st.cache_data
def get_data(symbol, timeframe, count):
    # get 10 GBPUSD D1 bars from the current day
    bars = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)

    
    # create DataFrame out of the obtained data
    df = pd.DataFrame(bars)

    # convert time in seconds into the datetime format
    df['time']=pd.to_datetime(df['time'], unit='s')

    return df




@st.cache_data
def bop_signal(df):
    bop = ta.TA.BOP(df)
    signal = []
    
    for i in range(len(df)):
        if bop[i] >= 0:
            signal.append('buy')
        elif bop[i] <= 0:
            signal.append('sell')
        else:
            signal.append(0)
    
    return signal[-1:]



@st.cache_data
def cci_signal(df):
    cci = ta.TA.CCI(df, period=13)
    signal = []
    
    for i in range(len(df)):
        if cci[i] > 0:
            signal.append('buy')
        elif cci[i] < 0:
            signal.append('sell')
        else:
            signal.append(0)
            
    return signal[-1:]


@st.cache_data
def fish_signal(df):
    fish = ta.TA.FISH(df, period=13)
    signal = []
    
    for i in range(len(df)):
        if fish[i] > 0:
            signal.append('buy')
        elif fish[i] < 0:
            signal.append('sell')
        else:
            signal.append(0)
            
    return signal[-1:]



@st.cache_data
def cmo_signal(df):
    cmo = ta.TA.CMO(df, period=28)


    signal = []
    
    for i in range(len(df)):
        if cmo.iloc[i] > 0:
            signal.append('buy')
        elif cmo.iloc[i] < 0:
            signal.append('sell')
        else:
            signal.append(0)
    return signal[-1:]



