# app1.py
import streamlit as st
import preprocessor1
import helper1
import matplotlib.pyplot as plt
import seaborn as sns

# ... (other imports)

# Set page configuration
st.set_page_config(page_title="Chat Analyzer", page_icon=":chart_with_upwards_trend:", layout="wide", initial_sidebar_state="expanded")

st.sidebar.title("Chat Analyzer")

def space():
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write('                ')
    with col2:
        st.write('                ')
    with col3:
        st.write('                ')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    
    df = preprocessor1.preprocess(data)

    #fetch unique users
    user_list = df['user'].unique().tolist()
    to_remove = 'group_notification'
    if to_remove in user_list:
        user_list.remove(to_remove)
    user_list.sort()
    user_list.insert(0, 'OverAll')

    selected_user = st.sidebar.selectbox('Show Analysis for', user_list)

    if st.sidebar.button('Show Analysis'):

        st.title("Top Statistics")

        num_messages, num_words, media_cnt, total_links = helper1.fetch_stats(selected_user, df)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header('Total Messages')
            st.header(num_messages)
        with col2:
            st.header('Total No. Words')
            st.header(num_words)
        with col3:
            st.header('Total Media Shared')
            st.header(media_cnt)
        with col4:
            st.header('Total Links Shared')
            st.header(total_links)

        space()
        space()
        space()

        # Finding the Busiest Users in the Group (GROUP LEVEL)
        if selected_user == 'OverAll':
            st.title('Most Busy Users')
            most_busy_ones, new_df = helper1.most_busy_users(df)

            fig, ax = plt.subplots()
            
            col1, col2 = st.columns(2)
            with col1:
                ax.barh(most_busy_ones.index, most_busy_ones.values, color='green')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
        
        space()
        space()
        space()

        # WordCloud
        if(selected_user != 'OverAll'):
            st.title("Word Cloud : " + selected_user)
        else:
            st.title('Word Cloud')
        df_wc = helper1.create_word_cloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
        
        space()
        space()
        space()

        # Most_Common_Words
        if(selected_user != 'OverAll'):
            st.title("Most Common Words : " + selected_user)
        else:
            st.title('Most Common Words')
        most_common_df = helper1.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df['word'], most_common_df['count'], color='green')
        st.pyplot(fig)

        space()
        space()
        space()

        # Monthly Activity
        if(selected_user != 'OverAll'):
            st.title("Monthly Activity : " + selected_user)
        else:
            st.title('Monthly Activity')
        monthly_activity_df = helper1.monthly_activity(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(monthly_activity_df['time'], monthly_activity_df['message'], color='green')
        plt.xticks(rotation=90)
        st.pyplot(fig)

        space()
        space()
        space()

        # Daily Activity
        if(selected_user != 'OverAll'):
            st.title("Daily Activity : " + selected_user)
        else:
            st.title("Daily Activity")
        daily_activity_df = helper1.daily_activity(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_activity_df['only_date'], daily_activity_df['message'], color='green')
        plt.xticks(rotation=90)
        st.pyplot(fig)

        space()
        space()
        space()

        # Weekly Activity
        st.title("Activity Map")
        col1, col2 = st.columns(2)

        # Most Busy Day
        weekly_activity_df = helper1.week_activity_map(selected_user, df)
        with col1:
            if(selected_user != 'OverAll'):
                st.header('Most Busy Day : ' + selected_user)
            else:
                st.header('Most Busy Day')
            fig, ax = plt.subplots()
            ax.barh(weekly_activity_df['day_name'], weekly_activity_df['message'], color='green')
            st.pyplot(fig)

        # Most Busy Month
        month_activity_df = helper1.month_activity_map(selected_user, df)
        with col2:
            if(selected_user != 'OverAll'):
                st.header('Most Busy Month : ' + selected_user)
            else:
                st.header('Most Busy Month')
            fig, ax = plt.subplots()
            ax.barh(month_activity_df['month'], month_activity_df['message'], color='yellow')
            st.pyplot(fig)

        # Hour Wise
        col1, col2 = st.columns(2)

        modt_busy_hour_df = helper1.most_busy_hour(selected_user, df)

        # Most Busy Hour
        with col1:
            if(selected_user != 'OverAll'):
                st.header('Most Busy Hour : ' + selected_user)
            else:
                st.header('Most Busy Hour')

            fig, ax = plt.subplots()
            ax.barh(modt_busy_hour_df['text_hour'], modt_busy_hour_df['message'], color='yellow')
            st.pyplot(fig)
        
        space()
        space()
        space()

        # Activity HeatMap
        activity_heatmap_df = helper1.activity_heatmap(selected_user, df)

        if(selected_user != 'OverAll'):
                st.header('Activity HeatMap : ' + selected_user)
        else:
            st.header('Activity HeatMap')

        fig, ax = plt.subplots()
        ax = sns.heatmap(activity_heatmap_df)
        ax.set_xlabel('Time', color='red', labelpad=15)
        ax.set_ylabel('Days', color='red', labelpad=10)

        st.pyplot(fig)

    # Sentiment Analysis (added after 'Show Analysis' button is clicked)
    if st.sidebar.button('Sentiment Analysis'):
        st.title("Sentiment Analysis")
        sentiment_counts = helper1.sentiment_analysis(selected_user, df)
        st.dataframe(sentiment_counts.rename(columns={'Sentiment_Count': 'Sentiment'})) 
        # Bar chart
        st.subheader("Sentiment Distribution")
        fig, ax = plt.subplots()
        sns.barplot(x='Sentiments', y='count', data=sentiment_counts, palette='viridis')
        st.pyplot(fig)

     # Emoji Analysis
        st.title("Emoji Analysis")
        emoji_df = helper1.emoji_visualization(selected_user, df)
        
        # Display DataFrame with emoji and their count
        st.subheader("Emoji Distribution")
        st.dataframe(emoji_df)

        # Bar chart for top emojis
        st.subheader("Top Emojis")
        fig, ax = plt.subplots()
        sns.barplot(x='Emoji', y='Count', data=emoji_df.head(10), palette='viridis')
        st.pyplot(fig)

    # Emotional analysis
        st.title("Emotional Tone Analysis")
        emotion_counts = helper1.emotion_analysis(selected_user, df)
        st.dataframe(emotion_counts.rename(columns={'Count': 'Emotion'}))

        # Pie chart
        st.subheader("Emotion Distribution")
        fig, ax = plt.subplots()

        # Customize the labels for better visibility
        labels = [f"{emotion} ({count})" for emotion, count in zip(emotion_counts['Emotions'], emotion_counts['count'])]

        # Use autopct='' to remove default percentage labels
        wedges, texts, autotexts = ax.pie(
            emotion_counts['count'],
            labels=labels,
            autopct='',
            startangle=90,
            colors=sns.color_palette('coolwarm'),
            textprops=dict(size=6),  # Adjust font size
        )

        # Add legends with labels and percentages
        ax.legend(wedges, labels, title="Emotions", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        ax.set_title("Emotion Distribution")

        # Set a custom layout for better visualization
        plt.tight_layout()
        st.pyplot(fig)

     