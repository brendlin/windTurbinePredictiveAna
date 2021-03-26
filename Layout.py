
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
from .DataManager import LoadFile
from .Callbacks import *
from .Styles import styles
from .Utils import TURBINES
from .Components import(
    main_graph,
    date_picker,hour_picker,minute_picker,go_button,
    speed_slider,
    header_infotip,
)
from .Plots import(
    GetPowerPlot,
)

storage = [
    dcc.Interval(id='interval-component',n_intervals=0,interval=2*1000), # in milliseconds
]

# Make the angular position indicators
wind_turbine_divs = []
for i in range(len(TURBINES)) :
    tmp = html.Div(children=[html.Img(id='turbine-%d-img'%(i),height='150px',width='150px',
                                      style=styles.turbine_style,src='assets/turbine.png'),
                             html.Img(id='wind-arrow-%d-img'%(i),height='150px',width='150px',
                                      style=styles.wind_style,src='assets/wind.png'),
                             html.Span('Wind direction indicated by red arrow.',
                                       className='tooltiptext'),
                             ],
                   style={'display':'inline-block','position':'relative'},
                   className='tooltip', # Meaning when you hover over this div, you get the text indicated in the Span above.
                   )
    wind_turbine_divs.append(tmp)
    if i+1 < NTURBINES :
        wind_turbine_divs.append(html.Div(style={'width':'10px','display':'inline-block'}))


# main layout
layout = html.Div( # Main Div
    children=[ # Main Div children
        html.Div( # Banner
            children=[
                html.H5(children=['Wind Turbine Predictive Maintenance',
                                  header_infotip,
                                  ]),
                *wind_turbine_divs,
                html.Div([ # settings div

                    html.Div([html.Div('Jump to date:',style=styles.jump_to_date),
                              date_picker,
                              hour_picker,html.Div(':',style=styles.hour_picker),
                              minute_picker,
                              go_button,
                              ],style=styles.settings_style,), # end of date-picking div

                    html.Div([html.Div('Simulation Speed:',style=styles.simulation_speed),
                              html.Div(speed_slider,style=styles.speed_slider)
                              ],
                             style=styles.settings_style,), # end of speed-picking div

                    html.Div([html.Div('Simulation Time:',style=styles.simulation_time_label),
                              html.Div(id='simulation-time',children='', # set up in callback
                                       style=styles.simulation_time),
                              ],style=styles.settings_style,
                             ), # end of simulation timestamp div

                ],), # end settings div
                html.Div(dcc.Graph(id='main-graph',figure=GetPowerPlot())),
            ],
            style={},
        ), # Banner End
        *storage,
    ], # Main Div children End
) # Main Div End
