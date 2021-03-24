
from .Utils import start_date

import dash_core_components as dcc
import dash_html_components as html

date_picker = dcc.DatePickerSingle(id='my-date-picker-single',
                                   min_date_allowed=start_date,
                                   max_date_allowed=start_date,
                                   initial_visible_month=start_date,
                                   date=start_date,
                                   disabled=False,
                                   )

speed_slider = dcc.Slider(id='speed-slider',min=0.5,max=6,step=None,value=0.5,
                          # Value equals number of 10-minute-intervals per second
                          marks={0.5: '5m', # 2 seconds between steps, 10 minutes per step
                                 1  :'10m',
                                 2  :'20m',
                                 6  : '1h',},
                          )

header_infotip = html.Div([html.Sup(u'\u2139',style={'background-color':'#c7ebe1'}),
                           html.Span('Hover over the "'+u'\u2139'+'" for more explanation.',
                                     className='tooltiptext',style={'font-size':'1.5rem'}),],
                          className='tooltip',
                          )

main_graph = dcc.Graph(id='display-tidepool-graph',
                       #config={'staticPlot':True,},
                       figure={'layout':{'margin':{'l':60, 'r':20, 't':27, 'b':20},
                                         'paper_bgcolor':'White','plot_bgcolor':'White',
                                         'yaxis':{'title':'BG (mg/dL)','range':[50,300],'linecolor':'Black','mirror':'ticks','hoverformat':'0.0f',},
                                         'xaxis':{'range':[1,100],'linecolor':'Black','mirror':'ticks'},
                                         }
                               },
                       style={'height': 400,}
                       )
