
import pytz

first_possible_date = '2017-01-02T00:00:00+01:00'
last_possible_date  = '2018-01-11T23:59:59+01:00'

TURBINES = ['R80711','R80721']#,'R80736','R80790']

TIMEZONE='Europe/Paris'
TZINFO = pytz.timezone(TIMEZONE)

TIMEIT = False

REALTIME_VARS = ['P_avg']
REALTIME_NDATAPOINTS = int( 60*60 /10. ) # 24 hours * 60 minutes
