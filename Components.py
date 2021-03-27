
from .Styles import styles
from .Utils import first_possible_date,last_possible_date

import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq

def GetTurbineAngularDiv(i_turb) :
    tmp = html.Div(children=[html.Img(id='turbine-%d-img'%(i_turb),height='150px',width='150px',
                                      style=styles.turbine_style,src='assets/turbine.png'),
                             html.Img(id='wind-arrow-%d-img'%(i_turb),height='150px',width='150px',
                                      style=styles.wind_style,src='assets/wind.png'),
                             ],
                   style={'display':'inline-block','position':'relative'},
                   )
    return tmp

date_picker = dcc.DatePickerSingle(id='my-date-picker-single',
                                   min_date_allowed=first_possible_date,
                                   max_date_allowed=last_possible_date,
                                   initial_visible_month=first_possible_date,
                                   date=first_possible_date,
                                   disabled=False,
                                   style={'vertical-align':'middle',
                                          'padding':'4px 4px',
                                          },
                                   )

hour_picker = dcc.Input(id='hour-picker',type='number',
                        placeholder='00',min=0,max=23,step=1,
                        style={'width':'50px','padding':'6px 6px','vertical-align':'middle',},
                        )

minute_picker = dcc.Input(id='minute-picker',type='number',
                          placeholder='00',min=0,max=50,step=10,
                          style={'width':'50px','padding':'6px 6px','vertical-align':'middle',},
                          )

go_button = html.Div(html.Button('Go',id='go-button',style={'width':'100%','padding':'0 0'}),
                     style={'display':'inline-block',
                            'width':'50px','vertical-align':'middle',
                            'padding':'0 0 0 8px',
                            },
                     )

speed_slider = dcc.Slider(id='speed-slider',min=1,max=5.5,step=None,value=1,
                          # Value equals number of 10-minute-intervals per second
                          marks={1: '5m/s', # 2 seconds between steps, 10 minutes per step
                                 2  :'10m/s',
                                 3.5  :'20m/s',
                                 5.5  : '1h/s',}
                          )
# Map between the visible slider positions and the actual value
# (the unit of the value is "number of 10-minute-slices displayed per second)
speed_slider_map = {1:0.5,
                    2:  1,
                    3.5:  2,
                    5.5:  6,}

pause_resume = html.Div(html.Button('Pause',id='pause-resume-button',
                                    n_clicks=0,
                                    style={'width':'100%',
                                           'height':'100%',
                                           'padding':'0px 12px 0px 12px',
                                           'border-radius':'4px',
                                           }),
                        style = {'height':'55px',
                                 'margin':'2px',
                                 'display':'inline-flex',
                                 'align-items':'center'},
                     )

toggle_realtime = html.Div([html.Div('Historical',style=styles.time_settings),
                            daq.ToggleSwitch(id='toggle-realtime',
                                             value=False,
                                             style=styles.toggle_realtime,
                                             color='#c35656',
                                             ),
                            html.Div('Real-time',style=styles.time_settings),
                            ],
                           style=styles.subsetting_style,
                           )

def MakeInfotip(text,hover_style={}) :
    _infotip = html.Div([html.Sup(u'\u2139',style={'background-color':'#c7ebe1'}),
                         html.Span(text,className='tooltiptext',style=hover_style),],
                        className='tooltip',
                        )
    return _infotip

angular_infotip = MakeInfotip('Wind direction indicated by red arrow.')
header_infotip  = MakeInfotip('Hover over the "'+u'\u2139'+'" for more explanation.',
                              hover_style={'font-size':'1.5rem'})

# This is the dummy graph that will replaced by various figures
main_graph = dcc.Graph(id='main-graph',
                       #config={'staticPlot':True,},
                       figure={'layout':{'margin':{'l':60, 'r':20, 't':27, 'b':20},
                                         'paper_bgcolor':'White','plot_bgcolor':'White',
                                         'yaxis':{'title':'Power [MW]','range':[0,300],
                                                  'linecolor':'Black','mirror':'ticks',
                                                  'hoverformat':'0.0f',},
                                         'xaxis':{'range':[1,100],'linecolor':'Black',
                                                  'mirror':'ticks'},
                                         }
                               },
                       style={'height': 400,}
                       )
