# import MetaTrader5 as mt5
# import PythonMetaTrader5 as mt5
import mt5
import pandas as pd
import pandas_ta as ta
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
    bop = ta.bop(df['open'], df['high'], df['low'], df['close'])
    signal = []
    
    for i in range(len(df)):
        if bop[i] >= 0:
            signal.append('buy')
        elif bop[i] <= 0:
            signal.append('sell')
        else:
            signal.append(0)
    
    return signal[-1:]



## Indicator: BRAR (BRAR)
######### IMPORTANT ########### (slow-entry)
@st.cache_data
def brar_signal(df):
    brar = ta.brar(df['open'], df['high'], df['low'], df['close'])
    signal = []
    
    for i in range(len(df)):
        if brar['AR_26'][i] > brar['BR_26'][i]:
            signal.append('buy')
        elif brar['AR_26'][i] < brar['BR_26'][i]:
            signal.append('sell')
        else:
            signal.append(0)
        
    return signal[-1:]


@st.cache_data
def cci_signal(df):
    cci = ta.cci(df['high'], df['low'], df['close'], length=13)
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
def cfo_signal(df):
    cfo = ta.cfo(df['close'], length=14)
    signal = []
    
    for i in range(len(df)):
        if cfo[i] > 0:
            signal.append('buy')
        elif cfo[i] < 0:
            signal.append('sell')
        else:
            signal.append(0)
    return signal[-1:]


@st.cache_data
def cksp_signal(df):
    cksp = ta.cksp(df['high'], df['low'], df['close'])
    signal = []
    
    for i in range(len(df)):
        if cksp['CKSPs_10_3_20'][i] > cksp['CKSPl_10_3_20'][i]:
            signal.append('buy')
        elif cksp['CKSPs_10_3_20'][i] < cksp['CKSPl_10_3_20'][i]:
            signal.append('sell')
        else:
            signal.append(0)
    return signal[-1:]


@st.cache_data
def cmf_signal(df):
    cmf = ta.cmf(df['high'], df['low'], df['close'], df['tick_volume'])
    signal = []
    
    for i in range(len(df)):
        if cmf[i] > 0:
            signal.append('buy')
        elif cmf[i] < 0:
            signal.append('sell')
        else:
            signal.append(0)
    return signal[-1:]

@st.cache_data
def cmo_signal(df):
    cmo = ta.cmo(df['close'], length=28)

    signal = []
    
    for i in range(len(df)):
        if cmo.iloc[i] > 0:
            signal.append('buy')
        elif cmo.iloc[i] < 0:
            signal.append('sell')
        else:
            signal.append(0)
    return signal[-1:]

@st.cache_data
def dm_signal(df):
    dm = ta.dm(df['high'], df['low'])
    signal = []
    
    for i in range(len(df)):
        if dm['DMP_14'].iloc[i] > dm['DMN_14'].iloc[i]:
            signal.append('buy')
        elif dm['DMP_14'].iloc[i] < dm['DMN_14'].iloc[i]:
            signal.append('sell')
        else:
            signal.append(0)
    return signal[-1:]


@st.cache_data
def dpo_signal(df):
    dpo = ta.dpo(df['close'], length=14)

    signal = []
    
    for i in range(len(df)):
        if dpo.iloc[i] > 0:
            signal.append('buy')
        elif dpo.iloc[i] < 0:
            signal.append('sell')
        else:
            signal.append(0)
    return signal[-1:]

@st.cache_data
def eom_signal(df):
    eom = ta.eom(df['high'], df['low'], df['close'], df['tick_volume'])

    signal = []
    
    for i in range(len(df)):
        if eom.iloc[i] > 0:
            signal.append('buy')
        elif eom.iloc[i] < 0:
            signal.append('sell')
        else:
            signal.append(0)
    return signal[-1:]

@st.cache_data
def eri_signal(df):
    eri = ta.eri(df['high'], df['low'], df['close'])
    signal = []
    
    
    for i in range(len(df)):
        # prev_bull = eri['BULLP_13'].iloc[ i - 1]
        # prev_bear = eri['BEARP_13'].iloc[ i - 1]
        
        if eri['BULLP_13'][i] > eri['BEARP_13'][i] and (eri['BULLP_13'][i] and eri['BEARP_13'][i]) > 0:
            signal.append('buy')
        elif eri['BEARP_13'][i] > eri['BULLP_13'][i] and (eri['BULLP_13'][i] and eri['BEARP_13'][i]) < 0:
            signal.append('sell')
        else:
            signal.append(0)
    return signal[-1:]

