# import MetaTrader5 as mt5
import PythonMetaTrader5 as mt5
import pandas as pd

mt5.initialize()

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
    print(result)
    
    
