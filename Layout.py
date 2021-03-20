
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

storage = [
    dcc.Interval(id='interval-component',n_intervals=0,interval=1*3000), # in milliseconds
]

layout = html.Div( # Main Div
    children=[ # Main Div children
        html.Div( # Banner
            children=[
                html.H5(children='Hello world!'),
                html.Div(children=[html.Img(id='turbine-img',height='150px',width='150px',
                                            style={'border-radius':'50%',
                                                   'position':'relative','left':'0px'},
                                            src='assets/turbine.png'),
                                   html.Img(id='wind-arrow-img',height='150px',width='150px',
                                            style={'border-radius':'50%',
                                                   'position':'absolute','left':'8px',
                                                   'transform':'rotate(0deg)'},
                                            src='assets/wind.png'),
                                   ],
                         style={},
                         ),
            ],
        ), # Banner End
        *storage,
    ], # Main Div children End
) # Main Div End
