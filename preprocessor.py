import pandas as pd
import re

def preprocess(data):
    pattern = r'\[(\d{2}/\d{2}/\d{4}), (\d{2}:\d{2}:\d{2})\] (.*?): (.*)'  #date time sender message
    
    tuples_list = re.findall(pattern, data, re.MULTILINE)   #pachi pandas dataframe ma convert garna break down to list of tuples
    
    df = pd.DataFrame(tuples_list, columns=['Date', 'Time', 'Sender', 'Message'])
    
    df['Date']  = pd.to_datetime(df['Date'], format='%d/%m/%Y')
    df['Time']  = pd.to_datetime(df['Time'], format='%H:%M:%S').dt.time
    
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month_name()
    df['Day'] = df['Date'].dt.day_name()
    df['Hour'] = pd.to_datetime(df['Time'], format='%H:%M:%S').dt.hour
    df['Minute'] = pd.to_datetime(df['Time'], format='%H:%M:%S').dt.minute
    
    return df