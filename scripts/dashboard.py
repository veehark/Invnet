import pandas as pd #dataframes
import yfinance as yf #stock data
#if Yahoo does not accept the use of the data, nasdaq-data-link
import numpy as np #data science
import matplotlib.pyplot as plt #calc
import plotly.express as px
import plotly.graph_objects as go
import pyfolio as pf
import dash_bootstrap_components as dbc
import dash
from dash import Dash, dcc, html, dash_table

app=Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

##########################################
#Data downloading
##########################################
ticker="^OMXHGI"

df=yf.download(ticker,
                     start=None,
                     end=None,
                     progress=False)

df=df.loc[:,["Adj Close"]]

##########################################
#Return calculations
##########################################
df["simple_rtn"]=df["Adj Close"].pct_change()
df["log_rtn"]=np.log(df["Adj Close"]/df["Adj Close"].shift(1))
df["cumulative_simple_rtn"]=(df["Adj Close"]/df.iloc[0]['Adj Close']-1)
df=df.dropna()
print(df.head())
##########################################
#Building graphs and tables
##########################################
table_desc=pd.DataFrame(df.loc[:,'simple_rtn'].describe(include='all'))

fig_price=px.line(df, y='Adj Close')
fig_price.update_layout(margin=dict(l=2, r=2, b=5, t=5),
                            xaxis=dict(showspikes=True,
                                        spikethickness=1,
                                        spikedash='dot',
                                        spikemode='across'))

fig_rtn=px.line(df, y='simple_rtn').update_traces(line_color='gray')
fig_rtn.update_layout(margin=dict(l=2, r=2, b=5, t=5),
                      xaxis=dict(showspikes=True,
                                    spikethickness=1,
                                    spikedash='dot',
                                    spikemode='across'))

fig_hist=px.histogram(df, x='simple_rtn', nbins=1000)
fig_hist.update_layout(margin=dict(l=2, r=2, b=5, t=5),
                       xaxis=dict(showspikes=True,
                                    spikethickness=1,
                                    spikedash='dot',
                                    spikemode='across'))

#Underwater plot
# Calculate drawdowns
cum_max = df['Adj Close'].cummax()
drawdown = (df['Adj Close'] - cum_max) / cum_max

# Create Plotly Express figure
fig_drawdown = px.area(df, color=drawdown < 0, 
              color_discrete_sequence=['blue', 'red'], 
              title='Underwater Plot of Asset Returns',
              labels={'index': 'Date', 'Adj Close': 'Adj Close'})
fig_drawdown.update_layout(yaxis_tickformat=',.2f',
                  xaxis_rangeslider_visible=True,
                  margin=dict(l=2, r=2, b=5, t=35))

##########################################
#Dash building
##########################################
app.layout=dbc.Container([
    dbc.Row([
        dbc.Col([
            dcc.Graph(figure=fig_price, config={'displayModeBar':False, 'scrollZoom':False, 'dragMode':False, 'editable':False})
        ], width=6),
        dbc.Col([
            dcc.Graph(figure=fig_rtn, config={'displayModeBar':False, 'scrollZoom':False, 'dragMode':False, 'editable':False})
        ], width=6)
    ], justify="between"),
    dbc.Row([
        dbc.Col([
            dcc.Graph(figure=fig_drawdown, config={'displayModeBar':False, 'scrollZoom':False, 'dragMode':False, 'editable':False})
        ], width=6),
        dbc.Col([
            dcc.Graph(figure=fig_hist, config={'displayModeBar':False, 'scrollZoom':False, 'dragMode':False, 'editable':False})
        ], width=6)
    ], justify="between"),
    dbc.Row([
        dbc.Col([
                dash_table.DataTable(table_desc.to_dict('records'))
            ], width=3),
    ])
])

if __name__ == '__main__':
    app.run_server()

