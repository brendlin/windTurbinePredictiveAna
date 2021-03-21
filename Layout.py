
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_table
import json
import os
import time
import pandas as pd

from app import app
from .Callbacks import *

NTURBINES=4

storage = [
    dcc.Interval(id='interval-component',n_intervals=0,interval=1*3000), # in milliseconds
]

turbine_style = style={'border-radius':'50%','position':'relative','left':'0px'}
wind_style={'border-radius':'50%','position':'absolute','left':'0px','transform':'rotate(0deg)'}

# Make the angular position indicators
wind_turbine_divs = []
for i in range(NTURBINES) :
    tmp = html.Div(children=[html.Img(id='turbine-%d-img'%(i),height='150px',width='150px',style=turbine_style,src='assets/turbine.png'),
                             html.Img(id='wind-arrow-%d-img'%(i),height='150px',width='150px',style=wind_style,src='assets/wind.png'),
                             ],
                   style={'display':'inline-block','position':'relative'}
                   )
    wind_turbine_divs.append(tmp)
    if i+1 < NTURBINES :
        wind_turbine_divs.append(html.Div(style={'width':'10px','display':'inline-block'}))


# main layout
layout = html.Div( # Main Div
    children=[ # Main Div children
        html.Div( # Banner
            children=[
                html.H5(children='Wind Turbine Predictive Maintenance'),
                *wind_turbine_divs,
            ],
            style={},
        ), # Banner End
        *storage,
    ], # Main Div children End
) # Main Div End
