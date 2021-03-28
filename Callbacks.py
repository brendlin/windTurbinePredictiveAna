
import numpy as np
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from datetime import datetime,timedelta

from .Utils import TURBINES,TIMEIT,TZINFO,REALTIME_NDATAPOINTS
from .Components import speed_slider_map
from app import app

from .Plots import(
    GetDataForRealTimePlots,
    UpdateRealtimePlot,
    GetPowerPlot,
)

# Update the wind and turbine angles
@app.callback([Output('interval-component','interval'),
               Output('interval-component','disabled'),
               Output('pause-resume-button','children'),
               ],
              [Input('speed-slider','value'),
               Input('toggle-realtime','value'),
               Input('pause-resume-button','n_clicks'),
               ],
              )
def ModifyUpdates(n_tenMinIntervalsPerSec,do_realtime,nPauseClicks) :

    # Calculate the desired interval time
    n_tenMinIntervalsPerSec = speed_slider_map[n_tenMinIntervalsPerSec]
    step_duration = (1/float(n_tenMinIntervalsPerSec))
    step_duration = max(step_duration,1) # in realtime seconds -- max one update every 1 sec
    step_duration = step_duration*1000 # in milliseconds

    # If realtime is turned off, then turn off the real-time updates.
    if not do_realtime :
        return step_duration,True,'[Disabled]' # (1000 years)*d*h*s*ms

    # If pause was clicked an even number of times, then do not update:
    if nPauseClicks%2 :
        return step_duration,True,'Resume'

    return step_duration,False,'Pause'


# This callback achieves the following:
# - (Triggered by a regular interval)
# SIMULATOR TIME:
#  - Initializes the simulator time, if not already initialized
#  - Increments the simulator by the delta time that has passed
#  - Changes the available dates in the simulator menu
# DATA:
#  - If the simulator data does not exist, load it from the csv files (only what you need)
#  - Update the data if we have moved into a different time range
#
@app.callback([Output('simulation-time','children'),
               Output('my-date-picker-single','initial_visible_month'),
               Output('my-date-picker-single','date'),
               Output('realtime-data-all','figure'),
               Output('realtime-index','children'),
               ],
              [Input('interval-component', 'n_intervals'),
               Input('go-button','n_clicks'),
               ],
              [State('speed-slider', 'value'),
               State('interval-component', 'interval'),
               State('simulation-time','children'),
               State('realtime-index','children'),
               State('my-date-picker-single','initial_visible_month'),
               State('my-date-picker-single','date'),
               State('hour-picker','value'),
               State('minute-picker','value'),
               State('realtime-data-all','figure'),
               ])
def UpdateEverything(n_intervals,
                     go_button_nclicks,
                     n_tenMinIntervalsPerSec,
                     realtimeStepDurationMs,simulation_time,
                     realtime_index,
                     date_picker_initvis_mo,
                     date_picker_date,
                     date_picker_hour,
                     date_picker_minute,
                     realtime_data_all,
                     ) :

    if TIMEIT :
        now = datetime.now()

    n_tenMinIntervalsPerSec = speed_slider_map[n_tenMinIntervalsPerSec]

    # If the go-button was pressed, use that to go to the date.
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if trigger_id == 'go-button' :
        #print(date_picker_date,type(date_picker_date))
        if date_picker_hour == None :
            date_picker_hour = 0
        if date_picker_minute == None :
            date_picker_minute = 0
        try :
            date_picker_dt = datetime.strptime(date_picker_date,'%Y-%m-%d %H:%M')
        except ValueError :
            date_picker_dt = datetime.strptime(date_picker_date,'%Y-%m-%d')

        tmp = datetime(year=date_picker_dt.year,month=date_picker_dt.month,
                       day=date_picker_dt.day,hour=date_picker_hour,
                       minute=10*(date_picker_minute//10))
        simulation_time_dt = TZINFO.localize(tmp)

        #print('setting date to',simulation_time_dt)
        simulation_time = simulation_time_dt.strftime('%Y-%m-%d %H:%M')

        # Have to also update the realtime index, now that we jumped in time.
        if realtime_data_all :
            # Takes some massaging to get this into the correct format to compare.
            tmp = simulation_time_dt.strftime('%Y-%m-%dT%H:%M:%S%z')
            tmp = tmp[:-2] + ':' + tmp[-2:]
            #print(realtime_data_all['data'][0]['x'][0])
            #print(tmp)
            realtime_index = np.searchsorted(realtime_data_all['data'][0]['x'],tmp)

    # Initialize the simulation time
    elif not simulation_time :
        now = datetime.now()
        # Now, instead it is in 2017, and rounded down the nearest 10 minutes.
        tmp = datetime(year=2017,month=now.month,day=now.day,
                       hour=now.hour,minute=10*(now.minute//10))
        simulation_time_dt = TZINFO.localize(tmp)
        simulation_time = simulation_time_dt.strftime('%Y-%m-%d %H:%M')
        date_picker_date = simulation_time
        date_picker_initvis_mo = simulation_time

    else :
        # Update the simulation time
        n_dataSteps = int(n_tenMinIntervalsPerSec*realtimeStepDurationMs*0.001)
        realtime_index += n_dataSteps
        add_time = timedelta(minutes=10*n_dataSteps)
        #print('10*',n_tenMinIntervalsPerSec,'*',realtimeStepDurationMs*0.001,'=',add_time)
        tmp = datetime.strptime(simulation_time,'%Y-%m-%d %H:%M') + add_time
        simulation_time_dt = TZINFO.localize(tmp)
        simulation_time = simulation_time_dt.strftime('%Y-%m-%d %H:%M')

    # Update the realtime data if it is not in the right time slice
    if realtime_data_all :
        realtime_data_start = datetime.strptime(realtime_data_all['data'][0]['x'][0],
                                                '%Y-%m-%dT%H:%M:%S%z').astimezone(TZINFO)
        realtime_data_end = datetime.strptime(realtime_data_all['data'][0]['x'][-1],
                                                '%Y-%m-%dT%H:%M:%S%z').astimezone(TZINFO)

        data_too_old = simulation_time_dt > realtime_data_end
        data_age_requirement = simulation_time_dt - timedelta(minutes=10*(REALTIME_NDATAPOINTS+5))
        data_too_young = realtime_data_start > data_age_requirement

    if (not realtime_data_all or data_too_old or data_too_young) :
        realtime_data_all,realtime_index = GetDataForRealTimePlots(simulation_time_dt)

    if TIMEIT :
        print('UpdateEverything took',datetime.now()-now)

    return simulation_time,date_picker_initvis_mo,date_picker_date,realtime_data_all,realtime_index


# Callback for which plot to show
# APPEARANCE:
#  - Update the wind and turbine angles
@app.callback([Output('simulation-time-display','children'),
               Output('main-graph','figure'),
               Output('historical-data-all','figure')] +
              list(Output('turbine-%d-img'%(i), 'style') for i in range(len(TURBINES))) +
              list(Output('wind-arrow-%d-img'%(i), 'style') for i in range(len(TURBINES))),
              [Input('simulation-time','children'),
               Input('toggle-realtime','value'),
               ],
              [State('realtime-data-all','figure'),
               State('realtime-index','children'),
               State('historical-data-all','figure')] +
              list(State('turbine-%d-img'%(i), 'style') for i in range(len(TURBINES))) +
              list(State('wind-arrow-%d-img'%(i), 'style') for i in range(len(TURBINES))),
              )
def DisplayPlot(simulation_time,do_realtime,realtime_data,realtime_index,historical_figures,
                *angle_styles) :

    if TIMEIT :
        now = datetime.now()

    #
    # Historical
    #
    if not do_realtime :

        if not historical_figures :
            historical_figures = GetPowerPlot()

        if TIMEIT :
            print('DisplayPlot (historical) took',datetime.now()-now)

        return simulation_time,historical_figures,historical_figures,*angle_styles

    #
    # Realtime
    #
    # From the realtime data (stored as a figure), construct the updating figure
    updating_data = UpdateRealtimePlot(realtime_data,'P_avg',realtime_index)

    for i in range(len(TURBINES)) :
        current_windloc = int(angle_styles[i+len(TURBINES)]['transform'].split('(')[1].split('deg')[0])
        current_windloc += int(np.random.normal(0,10))
        current_turbloc = int(current_windloc + np.random.normal(0,5))

        # wind loc
        angle_styles[i+len(TURBINES)]['transform'] = 'rotate({}deg)'.format(current_windloc)

        # turbine loc
        angle_styles[i]['transform'] = 'rotate({}deg)'.format(current_turbloc)

    if TIMEIT :
        print('DisplayPlot (realtime) took',datetime.now()-now)

    return simulation_time,updating_data,historical_figures,*angle_styles
