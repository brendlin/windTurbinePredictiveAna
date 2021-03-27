
import numpy as np
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from datetime import datetime,timedelta

from .Components import speed_slider_map
from app import app

NTURBINES=4

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
    step_duration = max(step_duration,0.5) # in realtime seconds -- max one update every 0.5 sec
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
# APPEARANCE:
#  - Update the wind and turbine angles
#
@app.callback([Output('simulation-time','children'),
               Output('my-date-picker-single','initial_visible_month'),
               Output('my-date-picker-single','date'),
               ] +
              list(Output('turbine-%d-img'%(i), 'style') for i in range(NTURBINES)) +
              list(Output('wind-arrow-%d-img'%(i), 'style') for i in range(NTURBINES)),
              Input('interval-component', 'n_intervals'),
              [State('speed-slider', 'value'),
               State('interval-component', 'interval'),
               State('simulation-time','children'),
               State('my-date-picker-single','initial_visible_month'),
               State('my-date-picker-single','date'),
               ] +
              list(State('turbine-%d-img'%(i), 'style') for i in range(NTURBINES)) +
              list(State('wind-arrow-%d-img'%(i), 'style') for i in range(NTURBINES)),
              )
def UpdateEverything(n_intervals,n_tenMinIntervalsPerSec,
                     realtimeStepDurationMs,simulation_time,
                     date_picker_initial_visible_month,
                     date_picker_start_date,
                     *styles) :

    n_tenMinIntervalsPerSec = speed_slider_map[n_tenMinIntervalsPerSec]

    # Initialize the simulation time
    if not simulation_time :
        now = datetime.now()
        # Now, instead it is in 2017, and rounded down the nearest 10 minutes.
        simulation_time = datetime(year=2017,month=now.month,day=now.day,
                                            hour=now.hour,minute=10*(now.minute//10))
        simulation_time = simulation_time.strftime('%Y-%m-%d %H:%M')
        date_picker_start_date = simulation_time

    else :
        # Update the simulation time
        add_time = timedelta(minutes=10*n_tenMinIntervalsPerSec*realtimeStepDurationMs*0.001)
        #print('10*',n_tenMinIntervalsPerSec,'*',realtimeStepDurationMs*0.001,'=',add_time)
        simulation_time = datetime.strptime(simulation_time,'%Y-%m-%d %H:%M') + add_time
        simulation_time = simulation_time.strftime('%Y-%m-%d %H:%M')

    for i in range(NTURBINES) :
        current_windloc = int(styles[i+NTURBINES]['transform'].split('(')[1].split('deg')[0])
        current_windloc += int(np.random.normal(0,10))
        current_turbloc = int(current_windloc + np.random.normal(0,5))

        # wind loc
        styles[i+NTURBINES]['transform'] = 'rotate({}deg)'.format(current_windloc)

        # turbine loc
        styles[i]['transform'] = 'rotate({}deg)'.format(current_turbloc)

    return simulation_time,simulation_time,simulation_time,*styles
