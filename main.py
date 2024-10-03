import MetaTrader5 as mt5
import pandas as pd
import pandas_ta as ta
import streamlit as st

import plotly.subplots as sp
import plotly.graph_objects as go

import feedparser

import indicators
import orders


st.set_page_config(page_title='Play with MetaTrader',
                   page_icon='💸',
                   layout='centered')
st.title(' Play with MetaTrader 💰')


mt5.initialize()




## Data Part
symbol_list = ['EURUSD', 'USDJPY', 'USDCNH', 'USDCHF', 'USDCAD', 'GBPUSD']
symbol = st.selectbox('Choose your symbol 💲', symbol_list)

select_tf = {
    '1d': mt5.TIMEFRAME_D1,
    '4h': mt5.TIMEFRAME_H4,
    '1h': mt5.TIMEFRAME_H1,
    '30m': mt5.TIMEFRAME_M30,
    '15m': mt5.TIMEFRAME_M15,
    '5m': mt5.TIMEFRAME_M5,
    '1m': mt5.TIMEFRAME_M1
}
selected_tf = st.selectbox('select the TimeFrame⌚', select_tf.keys())
timeframe = select_tf[selected_tf]

count = 100

df = indicators.get_data(symbol, timeframe, count)

st.dataframe(df,  use_container_width=True)

# Create subplots in a separate plane with different row heights
plt_df = sp.make_subplots(rows=3, cols=1, shared_xaxes=True,
                       subplot_titles=[f'{symbol} Forex Prices', 'Technical Indicators'],
                       vertical_spacing=0.1,
                       row_heights=[4, 0.15, 0.70])

# Add Stock Prices subplot
plt_df.add_trace(go.Candlestick(x=df.index,
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'],
                name='Forex Prices'), row=1, col=1)

plt_df.add_trace(go.Bar(x=df.index,
                     y=df['tick_volume']
                    ), row=3, col=1)

st.plotly_chart(plt_df)

## Indicators Part
bop = indicators.bop_signal(df)
brar = indicators.brar_signal(df)
cci = indicators.cci_signal(df)
cfo = indicators.cfo_signal(df)
cksp = indicators.cksp_signal(df)
cmf = indicators.cmf_signal(df)
dm = indicators.dm_signal(df)


lst_indi = ['BOP', 'CCI', 'CFO', 'CKSP', 'CMF', 'DM']
select_indicator = st.selectbox('Choose your indicator Signal 🎰', lst_indi)



if select_indicator == 'BOP':
    bop[-1:]
    # Plot the BOP indicator
    ind_bop = ta.bop(df['open'], df['high'], df['low'], df['close'])
    plot_bop = go.Figure(data=[go.Scatter(x=df.index, y=ind_bop)])
    plot_bop.update_layout(title='Balance of Power (BOP) Indicator', yaxis_title='BOP Value')
    st.plotly_chart(plot_bop)


if select_indicator == 'CCI':
    cci[-1:]
    cci_indi = ta.cci(df['high'], df['low'], df['close'], length=13)
    plt_cci = go.Figure(data=[go.Scatter(x=df.index, y=cci_indi)])
    plt_cci.update_layout(title='Commodity Channel Index (CCI)', yaxis_title='CCI Values')
    st.plotly_chart(plt_cci)


if select_indicator == 'CFO':
    cfo[-1:]
    ind_cfo = ta.cfo(df['close'], length=14)
    plt_cfo = go.Figure(data=[go.Scatter(x=df.index, y=ind_cfo)])
    plt_cfo.update_layout(title='Chande Forcast Oscillator (CFO)', yaxis_title='CFO Values')
    st.plotly_chart(plt_cfo)
    
if select_indicator == 'CKSP':
    cksp[-1:]
    ind_cksp = ta.cksp(df['high'], df['low'], df['close'])
    plt_cksp = go.Figure()
    plt_cksp.add_trace(go.Scatter(x=df.index,
                         y=ind_cksp['CKSPl_10_3_20'],
                         opacity=0.7,
                         line=dict(color='blue', width=2),
                         name='CKSPl'))
    plt_cksp.add_trace(go.Scatter(x=df.index,
                            y=ind_cksp['CKSPs_10_3_20'],
                            opacity=0.7,
                            line=dict(color='orange', width=2),
                            name='CKSPs'))
    st.plotly_chart(plt_cksp)
    
if select_indicator == 'CMF':
    st.write(cmf[-1:])
    ind_cmf = ta.cmf(df['high'], df['low'], df['close'], df['tick_volume'])
    plt_cmf = go.Figure(data=[go.Scatter(x=df.index, y=ind_cmf)])
    plt_cmf.update_layout(title='Chaikin Money Flow (CMF)', yaxis_title='CMF Values')
    st.plotly_chart(plt_cmf)


if select_indicator == 'DM':
    dm[-1:]
    ind_dm = ta.dm(df['high'], df['low'])
    plt_dm = go.Figure()
    plt_dm.add_trace(go.Scatter(x=df.index,
                         y=ind_dm['DMP_14'],
                         opacity=0.7,
                         line=dict(color='blue', width=2),
                         name='DMP_14'))
    plt_dm.add_trace(go.Scatter(x=df.index,
                            y=ind_dm['DMN_14'],
                            opacity=0.7,
                            line=dict(color='orange', width=2),
                            name='DMN_14'))
    st.plotly_chart(plt_dm)





# create orders
qty = st.slider('select the Lot percent', min_value=0.0, max_value=1.0, step=0.1)

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


if st.button('BUY'):
    orders.create_order(symbol,qty,buy_order, buy_price,buy_sl,buy_tp)

if st.button('SELL'):
    orders.create_order(symbol,qty,sell_order, sell_price,sell_sl,sell_tp)
    
    

###########################################################################
## the new's
rss_feeds = {
  "Select" : "",
  "FXNews-Group" : 'https://fxnewsgroup.com/feed/',
  "Action-Forex" : "https://www.actionforex.com/feed/",
  
  "Forex-News" : 'https://www.forexnews.world/feed/',
  "FX-Street" : 'https://www.fxstreet.com/rss/news',
  'Baby-Pips': 'https://www.babypips.com/news/feed.rss',
  'Market-Pluse': 'https://www.marketpulse.com/feed',
  'TradersUp_ar': 'https://www.tradersup.com/feed'
}

@st.cache_data(show_spinner='Loading the Forex news...')
def parse_feed(url):
    feed = feedparser.parse(url)
    articles = []
    for entry in feed.entries:
        article = {
            'title': entry.title,
            'link': entry.link,
            'description': entry.summary,
            'published_at': entry.published
        }
        articles.append(article)
        
    return articles

choose_news_feed = '**Select a news Feed:**'

rss_feed_selected = st.selectbox(choose_news_feed, rss_feeds.keys())
st.write(rss_feed_selected)

selected_rss_feed_url = rss_feeds[rss_feed_selected]

all_articles = []
articles = parse_feed(selected_rss_feed_url)
all_articles += articles

# sort articles by datetime
all_articles.sort(key=lambda article: article['published_at'], reverse=True)

#Display Articles
for article in all_articles:
  st.markdown(f"**{article['title']}**")
  st.markdown(f"{article['description']}", unsafe_allow_html=True)
  st.markdown(f"Published on: {article['published_at']}")
  st.markdown(f"Link: [More Info]({article['link']})")