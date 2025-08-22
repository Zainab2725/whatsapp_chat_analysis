import re
from textblob import TextBlob

def nlp(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users']== selected_user]
    
    def clean_data(message):
        message = re.sub(r'@[a-zA-Z0-9]+','',message)
        message = re.sub(r'#','',message)
        message = re.sub(r'https?://\S+','',message)

        return message
    
    df['message'] = df['message'].apply(clean_data)


    def getSubjectivity(text):
        return TextBlob.TextBlob(text).sentiment.subjectivity
    
    def getPolarity(text):
        return TextBlob.TextBlob(text).sentiment.polarity
    
    df['subjectivity']=df['message'].apply(getSubjectivity)
    df['polarity']=df['message'].apply(getPolarity)

    def getAnalysis(score):
        if score<0:
            return 'negative'
        elif score>0:
            return 'positive'
        else:
            return 'neutral'
        

    df['analysis'] = df['polarity'].apply(getAnalysis)

    return df

