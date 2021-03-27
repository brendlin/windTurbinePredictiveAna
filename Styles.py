
class styles_class() :
    def __init__(self) :
        pass

styles = styles_class()

styles.turbine_style = {'border-radius':'50%','position':'relative','left':'0px'}

styles.wind_style = {'border-radius':'50%','position':'absolute','left':'0px',
                     'transform':'rotate(0deg)','cursor': 'pointer'}

styles.right_angular_info = {'display':'inline-flex',
                             'justify-content':'space-evenly',
                             'flex-wrap':'wrap',
                             'background-color':'antiquewhite'}

styles.time_settings_div = {'width':'100%',
                            'display':'inline-flex',
                            'justify-content':'center',
                            }

styles.subsetting_style = {'border':'1px solid gray',
                           'border-radius':'4px','padding':'4px 4px 4px 4px',
                           'height':'45px',
                           'margin':'2px',
                           'display':'inline-flex',
                           'align-items':'center'}

styles.time_settings = {'padding':'4px 4px','text-align':'center',
                              'display':'inline-block'}

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

styles.toggle_realtime = {'padding':'4px 4px','text-align':'center',
                          'display':'inline-block',
                          }
