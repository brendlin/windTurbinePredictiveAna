
import pandas as pd
from plotly.subplots import make_subplots
from datetime import datetime,timedelta
import os
import numpy as np

from .Utils import TURBINES,TIMEIT,TIMEZONE,TZINFO,REALTIME_VARS,REALTIME_NDATAPOINTS

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

def GetAllDataForRealTimePlots(simulation_time_dt) :

    data = []

    if TIMEIT :
        now = datetime.now()

    for i,turbine in enumerate(TURBINES) :

        filenames = []

        # Month before, if we are less than one day into this month
        tmp = datetime(year=simulation_time_dt.year,month=simulation_time_dt.month,
                       day=1,hour=0,minute=0)
        start_of_month = TZINFO.localize(tmp)
        if (simulation_time_dt - start_of_month < timedelta(days=1)) :
            year = simulation_time_dt.year
            month = simulation_time_dt.month-1
            if month == 0 :
                year -= 1
                month = 12
            filenames.append('{}/{}/{:02d}/{}.csv.gz'.format('laHauteData',year,month,turbine))

        # the current month
        filenames.append('{}/{}/{:02d}/{}.csv.gz'.format('laHauteData',
                                                         simulation_time_dt.year,
                                                         simulation_time_dt.month,turbine))

        dfs = []
        for fname in filenames :
            #print(fname)
            if not os.path.isfile(fname) :
                continue
            dfs.append(pd.read_csv(fname,compression='gzip'))

        df = pd.concat(dfs)

        start_dt = pd.to_datetime(df['Date_time'].iloc[0] ).tz_convert(TIMEZONE)
        end_dt   = pd.to_datetime(df['Date_time'].iloc[-1]).tz_convert(TIMEZONE)
        theTimeAxis = pd.date_range(start=start_dt,end=end_dt,freq='10min')

        realtime_index = np.searchsorted(theTimeAxis,simulation_time_dt)
        #print('the index of the current simulation time is',realtime_index)

        # The first plot contains the time axis; the others do not.
        for j,var in enumerate(REALTIME_VARS) :
            plot = {'y':df[var],'name':'%s %s'%(turbine,var),}
            if i == 0 and j == 0 :
                plot['x'] = theTimeAxis

            data.append(plot)

    if TIMEIT :
        print('GetAllDataForRealTimePlots took',datetime.now()-now)

    return {'data':data},realtime_index


def GetTimeAxisForRealtimePlot(realtime_data) :
    # Return the time-series 'x' axis for realtime plots
    # The "x" (datetime) is only stored for the first plot..!
    return realtime_data['data'][0]['x']


def GetVarDataForRealtimePlot(realtime_data,i_turbine,variable) :
    # Get the plot that contains the data (in 'y')
    i_plot = i_turbine*len(REALTIME_VARS) + REALTIME_VARS.index(variable)
    return realtime_data['data'][i_plot]['y']


def UpdateRealtimePlot(realtime_data_all,variable,realtime_index) :

    fig = make_subplots(rows=1,cols=1,shared_xaxes=True)

    x = GetTimeAxisForRealtimePlot(realtime_data_all)

    for i_turbine in range(len(TURBINES)) :

        data_all_y = GetVarDataForRealtimePlot(realtime_data_all,i_turbine,variable)

        start_index = max(realtime_index-REALTIME_NDATAPOINTS+1,0)
        plot = {'x':         x[start_index:realtime_index+1],
                'y':data_all_y[start_index:realtime_index+1],
                'name':TURBINES[i_turbine]}

        fig.append_trace(plot,1,1)

    return fig


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
            start_dt = pd.to_datetime(df['Date_time'].iloc[0] ).tz_convert(TIMEZONE)
            end_dt   = pd.to_datetime(df['Date_time'].iloc[-1]).tz_convert(TIMEZONE)
            theTimeAxis = pd.date_range(start=start_dt,end=end_dt,freq='10min')
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
