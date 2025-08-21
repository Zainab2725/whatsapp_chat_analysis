import re
import pandas as pd 

def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[APap][Mm]\s-\s'
    message = re.split(pattern,data)[1:]
    dates = re.findall(pattern,data)
    df = pd.DataFrame({'user-message':message,'date':dates})
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%y, %I:%M %p - ')

    user = []
    messages = []

    for msg in df['user-message']:
        entry = re.split('([\w\W]+?):\s', msg)
        if entry[1:]:
            user.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            user.append('group_notification')
            messages.append(entry[0])

    df['users'] = user
    df['message'] = messages


    df.drop(columns=['user-message'],inplace=True)
    df['year']=df['date'].dt.year
    df['daily_dates'] = df['date'].dt.date   
    df['month']=df['date'].dt.month_name()
    df['month_num']=df['date'].dt.month
    df['day']=df['date'].dt.day
    df['day_name']=df['date'].dt.day_name()
    df['hour']=df['date'].dt.hour
    df['minute']=df['date'].dt.minute

    period = []
    for hour in df[['day_name','hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append("00" + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))


    df['period']=period

    return df