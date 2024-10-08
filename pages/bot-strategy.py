import streamlit as st
# import MetaTrader5 as mt5
# import PythonMetaTrader5 as pmt
# import pymt5 
# import pyomt5
import mt5_server as mt
import mt5 as mtt

import pandas as pd
# import pandas_ta as ta
import time
import plotly.subplots as sp
import plotly.graph_objects as go
import numpy as np

import indicators

# mt=pymt5.PyMT5()
st.set_page_config('Bot', page_icon='🤖')

st.title('Welcome to MetaTrader5 Trading-Bot 🤑')
  
mt5 = mt.MetaTrader5

mtt.initialize()


def get_data(symbol, timeframe, count):
                # get 10 GBPUSD D1 bars from the current day
                bars = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)

                
                # create DataFrame out of the obtained data
                df = pd.DataFrame(bars)

                # convert time in seconds into the datetime format
                df['time']=pd.to_datetime(df['time'], unit='s')

                return df            
  
            
            
            


            ## Creating orders
def create_order(symbol, qty, order_type, price, sl, tp):
                request = {
                    'action' : mt5.TRADE_ACTION_DEAL,
                    'symbol' : symbol,
                    'price' :   price,
                    'sl' : sl,
                    'tp' : tp,
                    'type' : order_type,
                    'volume' : qty,
                    'type_time' : mt5.ORDER_TIME_GTC,
                    'type_filling' : mt5.ORDER_FILLING_IOC,
                    'comment' : 'python open position'
                }
                
                result = mt5.order_send(request)
                return result
            
def posi(symbol):
                position = mt5.positions_get(symbol=symbol)
                
                signal= []
                if len(position) > 3:
                    signal.append('no')
                elif len(position) < 3:
                    signal.append('yes')
                    
                return signal
            
           
            
            
                
                
    


                ## Creating orders
def create_order(symbol, qty, order_type, price, sl, tp):
                    request = {
                        'action' : mt5.TRADE_ACTION_DEAL,
                        'symbol' : symbol,
                        'price' :   price,
                        'sl' : sl,
                        'tp' : tp,
                        'type' : order_type,
                        'volume' : qty,
                        'type_time' : mt5.ORDER_TIME_GTC,
                        'type_filling' : mt5.ORDER_FILLING_IOC,
                        'comment' : 'python open position'
                    }
                    
                    result = mt5.order_send(request)
                    return result
                
def posi(symbol):
                    position = mt5.positions_get(symbol=symbol)
                    
                    signal= []
                    if len(position) > 3:
                        signal.append('no')
                    elif len(position) < 3:
                        signal.append('yes')
                        
                    return signal
                
                
symbol_list = ['EURUSD', 'USDJPY', 'USDCNH', 'USDCHF', 'USDCAD', 'GBPUSD']
symbol = st.selectbox('Choose your symbol 💲', symbol_list)               
 
 
d1 = mt.MetaTrader5.TIMEFRAME_D1
h1 = mt.MetaTrader5.TIMEFRAME_H1
m30 = mt.MetaTrader5.TIMEFRAME_M30
m15 = mt.MetaTrader5.TIMEFRAME_M15
m5 = mt.MetaTrader5.TIMEFRAME_M5
m1 = mt.MetaTrader5.TIMEFRAME_M1



    
select_tf = {
    '1d': d1,
    # '4h': pyomt5.api.MT5TimeFrame.,
    '1h': h1,
    '30m': m30,
    '15m': mt5,
    '5m': m5,
    '1m': m1
}
selected_tf = st.selectbox('select the TimeFrame⌚', select_tf.keys())
tf = select_tf[selected_tf]


qty = st.slider('select the Lot percent', min_value=0.0, max_value=1.0, step=0.1)
 
count = 100
df = get_data(symbol,tf,count)
   


## Indicators Part
bop = indicators.bop_signal(df)
cci = indicators.cci_signal(df)
fish = indicators.fish_signal(df)
cmo = indicators.cmo_signal(df)

lst_indi = {'BOP':bop,
            'CCI':cci,
            'FISH':fish,
            'CMO':cmo}
select_indicator = st.selectbox('Choose your indicator Signal 🎰', lst_indi.keys())

signal = lst_indi[select_indicator]

lst_time = {
    '1min':60,
    '2min':120,
    '3min':180,
    '5min':300,
    '10min':600,
    '15min':900,
    '20min':1200,
    '30min':1800
    
}



time_wait = st.selectbox('time for strategy to wait', lst_time.keys())
wait = lst_time[time_wait]

     

if __name__ == '__main__':
    
    
    
    if 'button' not in st.session_state:
        st.session_state.button = False
        
    
    def click_button():
        st.session_state.button = not st.session_state.button

    btn_run = st.button('Run', on_click=click_button)


    if st.session_state.button:
        
        while btn_run:
            
            
            count = 100

            df = get_data(symbol,tf,count)
            
            
            buy_order = mt5.ORDER_TYPE_BUY
            sell_order = mt5.ORDER_TYPE_SELL

            buy_price = mt5.symbol_info_tick(symbol).ask
            sell_price = mt5.symbol_info_tick(symbol).bid
            sl_pct = 0.0003
            tp_pct = 0.0004
            buy_sl = buy_price * (1-sl_pct)
            buy_tp = buy_price * (1+tp_pct)
            sell_sl = sell_price * (1+sl_pct)
            sell_tp = sell_price * (1-tp_pct)
            
            pos = posi(symbol)
            
            
            
            
            for i in range(len(signal)):

                        if signal[i] == 'buy' and pos == ['yes']:
                            print(f'Buy {symbol} at {buy_price}')
                            st.write(f'Buy {symbol} at {buy_price}')
                            print(signal[i]) 
                            st.write(signal[i])               
                                        
                            create_order(symbol,qty,buy_order,buy_price,buy_sl,buy_tp)

                        elif signal[i] == 'sell' and pos == ['yes']:
                            print(f'Sell {symbol} at {sell_price}')
                            st.write(f'Sell {symbol} at {sell_price}')
                            
                            st.write(signal[i])            
                            create_order(symbol,qty,sell_order,sell_price,sell_sl,sell_tp)
                            
                        else:
                            if pos == 'no':
                                print(f'There is an signal for {symbol} please waite some minutes')  
                        
                        time.sleep(wait)
                        print(f'buy:{buy_price} / sell:{sell_price}')
                        st.write(f'buy:{buy_price} / sell:{sell_price}')
    else:
        st.write('Strategy Stopped')