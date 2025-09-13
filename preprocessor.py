import pandas as pd
import re

def normalize(text):
    if isinstance(text, str):
        # Remove all common invisible/Unicode control characters from WhatsApp exports
        text = re.sub(r'[\u200b-\u200f\u202a-\u202e\u202f\u00a0\u00ad\uFEFF\u2011]', '', text)
        return text.strip()
    return text

def preprocess(data):
    pattern = r'\[(\d{2}/\d{2}/\d{4}), (\d{2}:\d{2}:\d{2})\] (.*?): (.*)'  #date time sender message
    
    tuples_list = re.findall(pattern, data, re.MULTILINE)   #pachi pandas dataframe ma convert garna break down to list of tuples
    
    df = pd.DataFrame(tuples_list, columns=['Date', 'Time', 'Name', 'Message'])
    
    df['Date']  = pd.to_datetime(df['Date'], format='%d/%m/%Y')
    df['Time']  = pd.to_datetime(df['Time'], format='%H:%M:%S').dt.time
    
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month_name()
    df['Day'] = df['Date'].dt.day_name()
    df['Hour'] = pd.to_datetime(df['Time'], format='%H:%M:%S').dt.hour
    df['Minute'] = pd.to_datetime(df['Time'], format='%H:%M:%S').dt.minute
    
    # Normalize both columns
    df['Name'] = df['Name'].apply(normalize)
    df['Message'] = df['Message'].apply(normalize)

    # Remove empty messages
    notification_patterns = [
    r'^.* left$',          # X left
    r'^.* added .+$',      # X added Y
    r'^.* removed .+$',    # X removed Y
    r'^.* created this group$',
    r'^Waiting for this message\. This may take a while\.$',
    r'^.* changed their phone number.*$',
    r'^.* deleted this message.*$',
    r'^image omitted$',
    r'^document omitted$',
    r'^Tap to message new number$',
    r'^This message was deleted\.$',
    r'^You were added$',
    r'^You deleted this message\.$',
    r'^changed the subject from.*$',
    r"^changed this group's settings.*$",
    r'^changed the group description.*$',
    r"^changed this group's icon.*$",
    r'^Messages and calls are end-to-end encrypted.*$'
]

    # Apply regex filter
    notification_mask = ~df['Message'].str.match('|'.join(notification_patterns), case=False)
    df_cleaned = df[notification_mask].reset_index(drop=True)

    return df, df_cleaned
