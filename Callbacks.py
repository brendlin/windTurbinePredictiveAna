
import numpy as np
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app

NTURBINES=4

# Update the wind and turbine angles
@app.callback(list(Output('turbine-%d-img'%(i), 'style') for i in range(NTURBINES)) +
              list(Output('wind-arrow-%d-img'%(i), 'style') for i in range(NTURBINES)),
              Input('interval-component', 'n_intervals'),
              list(State('turbine-%d-img'%(i), 'style') for i in range(NTURBINES)) +
              list(State('wind-arrow-%d-img'%(i), 'style') for i in range(NTURBINES)),
              )
def UpdateEverything(n_intervals,*styles) :

    for i in range(NTURBINES) :
        current_windloc = int(styles[i+NTURBINES]['transform'].split('(')[1].split('deg')[0])
        current_windloc += int(np.random.normal(0,10))
        current_turbloc = int(current_windloc + np.random.normal(0,5))

        # wind loc
        styles[i+NTURBINES]['transform'] = 'rotate({}deg)'.format(current_windloc)

        # turbine loc
        styles[i]['transform'] = 'rotate({}deg)'.format(current_turbloc)

    return styles
