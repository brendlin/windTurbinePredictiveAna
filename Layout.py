
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
    GetTurbineAngularDiv,
    main_graph,
    date_picker,hour_picker,minute_picker,go_button,
    speed_slider,
    header_infotip,
    angular_infotip,
    toggle_realtime,
    pause_resume,
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
    tmp = html.Div(children=[GetTurbineAngularDiv(i),
                             html.Div([TURBINES[i],angular_infotip]),
                             ],
                   style={'display':'inline-block','position':'relative'},
                   # Below: when you hover over this div, you get the
                   # text indicated in the Span above.
                   )
    wind_turbine_divs.append(tmp)


# main layout
layout = html.Div( # Main Div
    children=[ # Main Div children
        html.Div( # Banner
            children=[

                html.Div(id='left-banner',children=[
                    html.H5(children=['Wind Turbine Predictive Maintenance',header_infotip,]),
                    toggle_realtime,
                         ],
                         style={'display':'inline-block','background-color':'aliceblue'},
                         className='five columns',
                         ),

                html.Div(id='right-angular-info',children=[*wind_turbine_divs,],
                         style=styles.right_angular_info,
                         className='seven columns',
                         ),
            ],
            style={},
            className='row',
        ), # Banner End

        html.Div( # another "row"
            html.Div([ # time settings div

                html.Div([html.Div('Jump to date:',style=styles.jump_to_date),
                          date_picker,
                          hour_picker,html.Div(':',style=styles.hour_picker),
                          minute_picker,
                          go_button,
                          ],style=styles.subsetting_style,), # end of date-picking div

                html.Div([html.Div('Simulation Speed:',style=styles.simulation_speed),
                          html.Div(speed_slider,style=styles.speed_slider)
                          ],
                         style=styles.subsetting_style,), # end of speed-picking div

                html.Div([html.Div('Simulation Time:',style=styles.simulation_time_label),
                          html.Div(id='simulation-time',children='', # set up in callback
                                   style=styles.simulation_time),
                          ],style=styles.subsetting_style,
                         ), # end of simulation timestamp div

                pause_resume,

                     ],
                     style=styles.time_settings_div,
                     #className='twelve columns',
            ), # end time settings div
        ), # end another "row"

        html.Div(dcc.Graph(id='main-graph',figure=GetPowerPlot())),
        *storage,
    ], # Main Div children End
    style={'text-align':'left',},
) # Main Div End
