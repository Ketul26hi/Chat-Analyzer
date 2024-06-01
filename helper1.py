from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import emoji
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def fetch_stats(selected_user, df):
    if selected_user != 'OverAll':
        df = df[df['user'] == selected_user]

    total_messages = df.shape[0]
    total_words = len(' '.join(df['message']).split())

    media_cnt = 0
    media = 'Media omitted'
    for message in df['message']:
        if media in message:
            media_cnt +=  1

    extractor = URLExtract()
    links = []
    for link in df['message']:
        links.extend(extractor.find_urls(link))
    for link in links:
        if link[0:4] != 'http':
            links.remove(link)

    return total_messages, total_words, media_cnt, len(links)


def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts()/df.shape[0])*100, 2).reset_index().rename(columns={'user': 'Name', 'count': 'Percent'})
    
    return x, df


def create_word_cloud(selected_user, df):
    if selected_user != 'OverAll':
        df = df[df['user'] == selected_user]
    
    df = df[df['user'] != 'group_notification']
    temp = df[df['message'] != '<Media omitted>\n']
    temp['message'] = df['message'].apply(lambda x: emoji.demojize(x))

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    special_symbols = ['!', '&', '#', ',', '*', '@', '$', '%', '-', '=', '+', '^', '_', '-', '–']

    words = []
    for msg in temp['message']:
        for word in msg.lower().split():
            if word not in stop_words:
                if word.isdigit() or word[0:4] == 'http' or word[0:1] == ':' or word in special_symbols:
                    continue
                elif word == 'ﷺ':
                        words.append('Rasulallah_SAW')
                elif word == 'اللّٰهَ' or word == 'اللّٰهِ':
                    words.append('Allah')
                elif word == 'الَّذِيۡنَ' or word == 'وَ' or word == 'مِّنۡ' or word == 'اِنَّ':
                    words.append('Quran_Ayah')
                else:
                    if len(word.split(':')) > 1:
                        words.append(word.split(':')[0])
                    else:
                        words.append(word)
        
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_for_wc = wc.generate(' '.join(words))
    
    return df_for_wc


def most_common_words(selected_user, df):
    if selected_user != 'OverAll':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    temp['message'] = temp['message'].apply(lambda x: emoji.demojize(x))

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    special_symbols = ['!', '&', '#', ',', '*', '@', '$', '%', '–', '=', '+', '^', '_']

    words = []
    for msg in temp['message']:
        for word in msg.lower().split():
            if word not in stop_words:
                if word.isdigit() or word[0:4] == 'http' or word[0:1] == ':' or word in special_symbols:
                    continue
                elif word == 'ﷺ' or word == 'rasoolallah':
                        words.append('Rasulallah_SAW')
                elif word == 'اللّٰهَ' or word == 'اللّٰهِ':
                    words.append('Allah')
                elif word == 'الَّذِيۡنَ' or word == 'وَ' or word == 'مِّنۡ' or word == 'اِنَّ':
                    words.append('Quran_Ayah')
                else:
                    if len(word.split(':')) > 1:
                        words.append(word.split(':')[0])
                    else:
                        words.append(word)

    new_df = pd.DataFrame(Counter(words).most_common(20)).rename(columns={0: 'word', 1: 'count'})
    new_df = new_df[new_df['word'] != "*"].head(20)
    
    return new_df


def monthly_activity(user, df):
    if user != 'OverAll':
        df = df[df['user'] == user]

    df = df.groupby(['year', 'num_month', 'month']).count()['message'].reset_index()

    timel = []
    for i in range(df.shape[0]):
        timel.append(df['month'][i] + '-' + str(df['year'][i]))

    df['time'] = timel 
        
    return df


def daily_activity(user, df):
    if user != 'OverAll':
        df = df[df['user'] == user]

    daily_timeline = df.groupby(['only_date']).count()['message'].reset_index()

    return daily_timeline


def week_activity_map(user, df):
    if user != 'OverAll':
        df = df[df['user'] == user]

    return df['day_name'].value_counts().reset_index().rename(columns={'count': 'message'})


def month_activity_map(user, df):
    if user != 'OverAll':
        df = df[df['user'] == user]

    return df['month'].value_counts().reset_index().rename(columns={'count': 'message'})


def most_busy_hour(user, df):
    if user != 'OverAll':
        df = df[df['user'] == user]

    return df.groupby(['text_hour']).count()['message'].reset_index().sort_values(['message'], ascending=False)


def activity_heatmap(user, df):
    if user != 'OverAll':
        df = df[df['user'] == user]

    activity_heatmap_df = df.pivot_table(index='day_name', columns='text_hour', values='message', aggfunc='count')

    return activity_heatmap_df


def sentiment_analysis(selected_user, df):
    sia = SentimentIntensityAnalyzer()
    df['compound'] = df['message'].apply(lambda x: sia.polarity_scores(x)['compound'])

    # Categorize sentiments
    df['Sentiment'] = df['compound'].apply(lambda score: 'Positive' if score >= 0.05 else ('Negative' if score <= -0.05 else 'Neutral'))

    # In sentiment_analysis function in helper1.py, make sure you have this line:
    sentiment_counts = df['Sentiment'].value_counts().reset_index().rename(columns={'index': 'Sentiment', 'Sentiment': 'Sentiments'})


    return sentiment_counts



#Emoji
def emoji_visualization(selected_user, df):
    if selected_user != 'OverAll':
        df = df[df['user'] == selected_user]

    df = df[df['user'] != 'group_notification']
    
    # Extract emojis from messages
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    # Count occurrences of each emoji
    emoji_counter = Counter(emojis)

    # Create DataFrame from the Counter
    emoji_df = pd.DataFrame(list(emoji_counter.items()), columns=['Emoji', 'Count'])

    # Sort DataFrame by count in descending order
    emoji_df = emoji_df.sort_values(by='Count', ascending=False)

    return emoji_df

def extract_emojis(text):
    return [c for c in text if c in emoji.EMOJI_DATA]

# Emotional Analysis
def emotion_analysis(selected_user, df):
    sia = SentimentIntensityAnalyzer()
    df['compound'] = df['message'].apply(lambda x: sia.polarity_scores(x)['compound'])

    # Map sentiment scores to emotions
    df['Emotion'] = df['compound'].apply(lambda score: map_to_emotion(score))

    # In emotion_analysis function in helper1.py, make sure you have this line:
    emotion_counts = df['Emotion'].value_counts().reset_index().rename(columns={'index': 'Emotion', 'Emotion': 'Emotions'})

    return emotion_counts

def map_to_emotion(score):
    if score >= 0.5:
        return 'Very Happy'
    elif 0.3 <= score< 0.5:
        return 'Happy'
    elif -0.3 < score < 0.3:
        return 'Neutral'
    elif -0.5 <= score < -0.3:
        return 'Sad'
    else:
        return 'Very Sad'
    
