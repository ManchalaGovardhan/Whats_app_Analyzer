import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns 
st.sidebar.title("Whatsapp Chat Analyzer")
Uploaded_file=st.sidebar.file_uploader("choose a file")
if Uploaded_file is not None:
    bytes_data=Uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    df=preprocessor.preprocess(data)
  
    # fetch user_list
    user_list=df['users'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_User=st.sidebar.selectbox("show analysis wrt",user_list)
    if st.sidebar.button("show Analysis"):
        num_messages,words,num_meadia_messages,num_links=helper.fetch_stats(selected_User,df)
        st.title("Top statistics")
        col1,col2,col3,col4=st.columns(4)
        
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2: 
            st.header("Total Words")
            st.title(words)
        with col3: 
            st.header("Total meadia shared")
            st.title(num_meadia_messages)
        with col4:
            st.header("Links Shared")
            st.title(num_links)
        #monthly timeline
        st.title('Monthly Timeline')
        timeline=helper.monthly_timeline(selected_User,df)
        fig,ax=plt.subplots()
        ax.plot(timeline['time'],timeline['message'])
        plt.xticks(rotation='vertical')

        st.pyplot(fig)
        #daily timeline
        st.title("Datily Timeline")
        daily_timeline=helper.daily_timeline(selected_User,df)
        fig,ax=plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'],color='black')
        plt.xticks(rotation='vertical')

        st.pyplot(fig)
        # activity map
        st.title('Activity Map')
        col1,col2 =st.columns(2)
        with col1:
            st.header("Most busy day")
            busy_day=helper.week_activity_map(selected_User,df)
            fig,ax=plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            st.pyplot(fig)
        with col2:
            st.header("Most busy month")
            busy_month=helper.month_activity_map(selected_User,df)
            fig,ax=plt.subplots()
            ax.bar(busy_month.index,busy_month.values)
            st.pyplot(fig)
        st.title("weakly activity Map")
        User_heatmap=helper.activity_heatmap(selected_User,df)
        fig,ax=plt.subplots()
        ax=sns.heatmap(User_heatmap)
        st.pyplot(fig)
      
        

        if selected_User=='Overall':
            st.title('Most Busy Users:')
            x,new_df=helper.most_busy_users(df)
            fig,ax=plt.subplots()
          
            col1,col2=st.columns(2)
            with col1:
                ax.bar(x.index,x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
    #word cloud
    st.title('Word cloud')
    df_wc=helper.create_wordcloud(selected_User,df)
    fig,ax=plt.subplots()
    ax.imshow(df_wc)
    st.pyplot(fig)

    #most common words
    most_common_df=helper.most_common_words(selected_User,df)
    fig,ax=plt.subplots()
    ax.barh(most_common_df[0],most_common_df[1])
    plt.xticks(rotation='vertical')
    st.title('Most common used words')
    st.pyplot(fig)
    #emoji analysis
    emoji_df=helper.emoji_helper(selected_User,df)
    st.title('Emoji Analysis')
    col1,col2=st.columns(2)
    with col1:
        st.dataframe(emoji_df)
    with col2:
        if emoji_df.empty or emoji_df[0].head(10).isnull().all():
            st.write("No emojis to display.")
        else:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(10), labels=emoji_df[0].head(10), autopct="%0.2f")
            st.pyplot(fig)
        fig,ax=plt.subplots()
    
        
               