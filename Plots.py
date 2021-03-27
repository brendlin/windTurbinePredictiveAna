
import pandas as pd
from plotly.subplots import make_subplots
from datetime import datetime

from .Utils import TURBINES,TIMEIT

def UpdateLayout(fig) :

    #fig.update_yaxes(range=[50,300], row=1, col=1)
    fig.update_yaxes(gridcolor='LightGray',mirror='ticks',showline=True,linecolor='Black', row=1, col=1)
    fig.update_yaxes(gridcolor='LightGray',mirror='ticks',showline=True,linecolor='Black', row=2, col=1)
    fig.update_yaxes(hoverformat='0.0f',row=1,col=1)
    fig.update_yaxes(hoverformat='0.0f',row=2,col=1)
    fig.update_xaxes(gridcolor='LightGray',mirror='ticks',showline=True,linecolor='Black')
    fig.update_layout(margin=dict(l=20, r=20, t=27, b=20),paper_bgcolor="White",plot_bgcolor='White')
    #fig.update_layout(showlegend=False)

    return

def GetPowerPlot() :

    fig = make_subplots(rows=1,cols=1,shared_xaxes=True)
    fig.update_yaxes(title_text="Power [MW]", row=1, col=1)
    UpdateLayout(fig)

    if TIMEIT :
        now = datetime.now()

    for i,turbine in enumerate(TURBINES) :
        #print('Processing turbine %s'%(turbine))
        df = pd.read_csv('laHauteData/%s_all.csv.gz'%(turbine),compression='gzip')

        if i == 0 :
            #theTimeAxis = pd.to_datetime(df['Date_time'],infer_datetime_format=True)

            # Instead of converting everything to datetime, assume it is in 10min intervals
            # and recreate the date_range instead of converting the times.
            theTimeAxis = pd.date_range(start=df['Date_time'].iloc[0],
                                        end=df['Date_time'].iloc[-1],freq='10min')
            #print("length of data is",theTimeAxis.shape)

        plot = {'x':theTimeAxis,
                'y':df['P_avg'],
                'name':turbine,
                }
        fig.append_trace(plot,1,1)

    del df
    del theTimeAxis

    if TIMEIT :
        print('GetPowerPlot took',datetime.now()-now)

    return fig
