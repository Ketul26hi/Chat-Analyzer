import re
import pandas as pd

def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}\s-\s'
    messages = re.split(pattern, data)
    dates = re.findall(pattern, data)

    messages = messages[2:]
    dates = dates[1:]

    time = []

    for i in range(len(dates)):
        time.append(dates[i].split()[2])
        dates[i] = " ".join(dates[i].split()[0:2])

    for i in range(len(dates)):
        if (time[i] == 'AM') and int(dates[i].split()[1].split(':')[0]) == 12:
            dates[i] = dates[i].split()[0].split(',')[0] + ' ' + '00' + ':'+dates[i].split()[1].split(':')[1]
        if (time[i] == 'PM') and int(dates[i].split()[1].split(':')[0]) != 12:
            dates[i] = dates[i].split()[0].split(',')[0] + ' ' + str(int(dates[i].split()[1].split(':')[0])+12)+':'+dates[i].split()[1].split(':')[1]
    
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    df['message_date'] = pd.to_datetime(df['message_date'], format='mixed')

    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    text_messages = []

    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            text_messages.append(entry[2])
        else:
            users.append('group_notification')
            text_messages.append(entry[0])

    am_pm = {0: '12-AM', 1: '01-AM', 2: '02-AM', 3: '03-AM', 4: '04-AM', 5: '05-AM', 6: '06-AM', 7: '07-AM', 8: '08-AM', 9: '09-AM', 10: '10-AM', 11: '11-AM', 12: '12-PM', 13: '01-PM', 14: '02-PM', 15: '03-PM', 16: '04-PM', 17: '05-PM', 18: '06-PM', 19: '07-PM', 20: '08-PM', 21: '09-PM', 22: '10-PM', 23: '11-PM'}

    df['user'] = users
    df['message'] = text_messages
    df.drop(columns=['user_message'], inplace=True)

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['num_month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    hour_am_pm = []
    for i in df['hour']:
        hour_am_pm.append(am_pm[i])
    df['text_hour'] = hour_am_pm
    df['only_date'] = df['date'].dt.date

    df.drop(columns=['date'], inplace=True)

    return df