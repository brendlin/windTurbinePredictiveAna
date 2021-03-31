#!/usr/bin/env python3

import pandas as pd
import numpy as np
import math
import os

#
# Download the data using:
# 2017 data:
# wget https://opendata-renewables.engie.com/media/datasets/01c55756-5cd6-4f60-9f63-2d771bb25a1a.zip 
# unzip 01c55756-5cd6-4f60-9f63-2d771bb25a1a.zip
#

df = pd.read_csv("la-haute-borne-data-2017-2020.csv",delimiter=';')
df = df.sort_values(by='Date_time')

df['Va_avg_composite'] = df['Va_avg'].fillna(df['Va1_avg'])
df['Wa_reconstructed'] = (df['Va_avg_composite'] + df['Ya_avg'])%360
df['Date_time_dt'] = pd.to_datetime(df['Date_time'],utc=True,
                                    infer_datetime_format=False).dt.tz_convert('Europe/Paris')

def CleanDuplicatesAndAddMissingTimesteps(_df,debug=True) :

    # Drop (both) rows where Date_time is identical (since this is not very reliable data)
    df_ret = _df.drop_duplicates(subset=['Date_time'],keep=False)
    
    if debug :
        print('Making dataset with 10 min intervals between',
              df_ret['Date_time'].iloc[0],'and',
              df_ret['Date_time'].iloc[-1])

    # Make a date range from the start to the end, in 10 min intervals
    # (which is how the data is structured)
    df_range = pd.DataFrame({'Date_time':pd.date_range(start=df_ret['Date_time_dt'].iloc[0],
                                                       end=df_ret['Date_time_dt'].iloc[-1],
                                                       freq='10min')})

    # Perform a left join, so that missing items in dataset are set to Null
    # (but we have full time coverage.)
    df_ret = df_range.set_index('Date_time').join(df_ret.set_index('Date_time_dt'))

    return df_ret

columns_to_save = [
    'Date_time',
    'Ya_avg',
    'Va_avg_composite',
    'Wa_reconstructed',
    'Ws1_avg',
    'Ws2_avg',
    'P_avg',
]

#
# Save the wind turbine data in monthly chunks
#
for wt in set(df['Wind_turbine_name']) :
    print(wt)
    for yr in set(df['Date_time_dt'].dt.year) :
        for mo in range(1,13) :

            # Make selection
            selection = (df['Date_time_dt'].dt.year == yr) & (df['Date_time_dt'].dt.month == mo)
            selection = selection & (df['Wind_turbine_name'] == wt)
            if not any(selection) :
                continue

            # Make new directory
            dirpath = '{:02d}/{:02d}'.format(yr,mo)
            if not os.path.exists(dirpath) :
                os.makedirs(dirpath)

            df_tmp = df[selection]
            df_tmp = CleanDuplicatesAndAddMissingTimesteps(df_tmp,debug=(mo < 3))

            df_tmp.to_csv('%s/%s.csv.gz'%(dirpath,wt),
                          columns=columns_to_save,index=False,
                          float_format='%.3g',compression='gzip')

columns_to_save = [
    'Date_time',
    'P_avg',
]

# Save the full span of wind turbine data
for wt in set(df['Wind_turbine_name']) :
    print(wt)
    # Make selection
    selection = (df['Wind_turbine_name'] == wt)
    if not any(selection) :
        continue

    df_tmp = df[selection]
    df_tmp = CleanDuplicatesAndAddMissingTimesteps(df_tmp,debug=True)
    
    df_tmp.to_csv('%s_all.csv.gz'%(wt),
                  columns=columns_to_save,index=False,
                  float_format='%.3g',compression='gzip')
