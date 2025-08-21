from urlextract import URLExtract 
from collections import Counter
from wordcloud import WordCloud
import pandas as pd 
import emoji 


extract = URLExtract()

def fetch_stats(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users']==selected_user]

    total_message = df.shape[0]

    words = []
    for message in df['message']:
          words.extend(message.split())

    media_num = df[df['message'] == '<Media omitted>\n'].shape[0]  

    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))


    return total_message,len(words),media_num,len(links)


def most_active_user(df):
    for_graph_df = df['users'].value_counts().head()
    for_table_df = round((df['users'].value_counts()/df['users'].shape[0])*100,2).reset_index().rename(columns={'index':'name','user':'percentage'})
    return for_graph_df,for_table_df


def create_word_cloud(selected_user,df):
    f = open('stop_hinglish.txt','r')
    stop_words = f.read()
    
    if selected_user != 'Overall':
        df = df[df['users']==selected_user]
    
    temp = df[df['users']!='group_notification']
    temp = temp[temp['message']!='<Media omitted>\n']


    def remove_stop_words(message):
          words = []
          for word in message.lower().split():
                if word not in stop_words:
                     words.append(word)
          return " ".join(words)

    wc = WordCloud(width=500,height=500,random_state=21,max_font_size=119,background_color='white')
    temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep =' '))
    
    return df_wc

def most_common_words(selected_user,df):

    f = open('stop_hinglish.txt','r') 
    stop_words = f.read().split()

    if selected_user != 'Overall':
        df = df[df['users']== selected_user]


    temp = df[df['users']!='group_notification']
    temp = temp[temp['message']!='<Media omitted>\n']

    words = []
    for message in temp['message']:
            for word in message.lower().split():
                    if word not in stop_words:
                           words.append(word)
             

 
    return pd.DataFrame(Counter(words).most_common(20), columns=['word','count'])



def common_used_emojis(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users']== selected_user]

    emojis = []
    for message in df['message']:
          emojis.extend([c for c in message if c in emoji.EMOJI_DATA]) 
     
    emoji_df = pd.DataFrame(Counter(emojis).most_common(20), columns=['emoji','count'])
    return emoji_df

def montly_timeline(selected_user,df):
     if selected_user != 'Overall':
        df = df[df['users']== selected_user]
     timeline = df.groupby(['year','month_num','month']).count()['message'].reset_index()
     time = []
     for i in range(timeline.shape[0]):
          time.append(timeline['month'][i]+", "+str(timeline['year'][i]))
    
     timeline['time'] = time

     return timeline

def day_timeline(selected_user,df):
     if selected_user != 'Overall':
        df = df[df['users']== selected_user]

     return df['day_name'].value_counts()

def month_activity(selected_user,df):
     if selected_user != 'Overall':
        df = df[df['users']== selected_user]

     return df['month'].value_counts()


def daily_timeline(selected_user,df):
     if selected_user != 'Overall':
        df = df[df['users']== selected_user]
     timeline = df.groupby(['daily_dates']).count()['message'].reset_index()

     return timeline

def heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users']== selected_user]
    user_heatmap= df.pivot_table(index='day',columns='period',values='message',aggfunc='count').fillna(0) 
    return user_heatmap
          