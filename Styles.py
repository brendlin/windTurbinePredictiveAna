
class styles_class() :
    def __init__(self) :
        pass

styles = styles_class()

styles.turbine_style = {'border-radius':'50%','position':'relative','left':'0px'}

styles.wind_style={'border-radius':'50%','position':'absolute','left':'0px',
                   'transform':'rotate(0deg)','cursor': 'pointer'}

styles.settings_style = {'border':'1px solid gray',
                         'border-radius':'4px','padding':'4px 4px 4px 4px',
                         'height':'45px',
                         'margin':'2px',
                         'display':'inline-flex',
                         'align-items':'center'}

styles.jump_to_date = {'padding':'4px 4px','text-align':'center',
                       'display':'inline-block'}

styles.hour_picker = {'width':'10px','text-align':'center',
                      'display':'inline-block'}

styles.simulation_speed = {'padding':'4px 4px','text-align':'center','vertical-align':'middle',
                           'display':'inline-block'}

styles.speed_slider = {'width':'230px','padding-top':'5px','vertical-align':'middle',
                    'display':'inline-block'}

styles.simulation_time_label = {'padding':'4px 4px','text-align':'center',
                                'display':'inline-block'}

styles.simulation_time = {'display':'inline-block','padding':'4px 4px'}
