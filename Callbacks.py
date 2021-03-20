
import numpy as np
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app

# Update the wind and turbine angles
@app.callback([Output('turbine-img', 'style'),
               Output('wind-arrow-img', 'style'),
               ],
              Input('interval-component', 'n_intervals'),
              [State('turbine-img', 'style'),
              State('wind-arrow-img', 'style'),
              ]
              )
def UpdateEverything(n_intervals,turbine_style,wind_style) :
    current_windloc = int(wind_style['transform'].split('(')[1].split('deg')[0])
    current_windloc += int(np.random.normal(0,10))
    current_turbloc = int(current_windloc + np.random.normal(0,5))

    wind_style['transform'] = 'rotate({}deg)'.format(current_windloc)
    turbine_style['transform'] = 'rotate({}deg)'.format(current_turbloc)

    return turbine_style,wind_style
