import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import preprocessor
import helper 
import sentimental_analysis
plt.rcParams['font.family'] = 'Segoe UI Emoji'


plt.style.use('fivethirtyeight')

st.sidebar.title('Whatsapp Chat Analysis')

uploaded_file = st.sidebar.file_uploader('Choose a file')
if uploaded_file is not None:
    bytes_data= uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocess(data)


    user_list = df['users'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox('Show analysis wrt',user_list)

    if st.sidebar.button('Show Analysis'):
        
        st.title('TOP STATISTICS')

        total_message,num_of_words,media_num,links_num = helper.fetch_stats(selected_user,df)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header('Total Messages')
            st.title(total_message)
        with col2:
            st.header('Total Words')
            st.title(num_of_words)
        
        with col3:
            st.header('Media Shared')
            st.title(media_num)
        with col4:
            st.header('Links Shared')
            st.title(links_num)

        st.header('Montly Timeline')
        montly_timeline = helper.montly_timeline(selected_user,df)
        fig, ax = plt.subplots()
        ax.plot(montly_timeline['time'],montly_timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.header('Montly Activity')
        month_activity = helper.month_activity(selected_user,df)
        fig, ax = plt.subplots()
        ax.bar(month_activity.index, month_activity.values,color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        st.title('Activities')

        
        col1, col2, = st.columns(2)

        with col1:
            st.header('Week Activity')
            day_timeline = helper.day_timeline(selected_user,df)
            fig, ax = plt.subplots()
            ax.bar(day_timeline.index, day_timeline.values,color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header('Daily Activity')
            daily_timeline = helper.daily_timeline(selected_user,df)
            fig, ax = plt.subplots()
            ax.plot(daily_timeline['daily_dates'],daily_timeline['message'])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        

        if selected_user == 'Overall':
            st.title('Most Active User')
            most_active_user , most_active_user_table_per = helper.most_active_user(df)
            fig, ax = plt.subplots()
            
            col1, col2 = st.columns(2)

            with col1:
                ax.bar(most_active_user.index,most_active_user.values,color='grey')  
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(most_active_user_table_per)

        st.title('WordCloud')
        df_wc = helper.create_word_cloud(selected_user,df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        st.title('Common Words')

        col1, col2, col3, col4, col5 = st.columns(5)
        cols = [col1, col2, col3, col4, col5]

        most_common_words = helper.most_common_words(selected_user, df)

        
        for i, row in most_common_words.head(5).iterrows():
            with cols[i]:
                st.header(row[0])
                st.title(row[1])
  

        
        fig, ax = plt.subplots()
        ax.barh(most_common_words['word'], most_common_words['count'],color='orange')
        st.pyplot(fig)
        
        st.title('Common Emojis')
        emoji_df = helper.common_used_emojis(selected_user,df).head()
        
        fig, ax = plt.subplots()
        ax.pie(emoji_df['count'],labels=emoji_df['emoji'], autopct='%0.2f')
        st.pyplot(fig)

        st.title("Weekly Activity Map")
        fig, ax = plt.subplots()
        activity = helper.heatmap(selected_user,df)
        ax = sns.heatmap(activity)
        st.pyplot(fig)

        df=sentimental_analysis.nlp(selected_user,df)
        st.title('Sentimental Analysis')
        fig, ax = plt.subplots()

        for i in range(df.shape[0]):
            ax.scatter(df['polarity'].iloc[i],df['subjectivity'].iloc[i],color='Blue')

        plt.xlabel('Polarity')
        plt.ylabel('Sujectivity')
        st.pyplot(fig)

        positive_msg = round(((df[df['analysis']=='positive'].shape[0])/(df.shape[0]))*100,2)
        neutral_msg = round(((df[df['analysis']=='neutral'].shape[0])/(df.shape[0]))*100,2)
        negative_msg = round(((df[df['analysis']=='negative'].shape[0])/(df.shape[0]))*100,2)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.header('Positive MSG')
            st.title(str(positive_msg)+'%')

        with col2:
            st.header('Neutral MSG')
            st.title(str(neutral_msg)+'%')

        with col3:
            st.header('Negative MSG')
            st.title(str(negative_msg)+'%')

        fig, ax = plt.subplots()
        plt.xlabel('Sentiment')
        plt.ylabel('Counts')
        df['analysis'].value_counts().plot(kind='bar')
        st.pyplot(fig)



        




       
        


            


