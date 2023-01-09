import json
import re
import sqlite3

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from tweepy import api


@csrf_exempt
@login_required
def word_cloud(request):
    # Get the maximum number of words to return
    num_words = request.POST.get('num_words')
    # Get the response format (JSON or CSV)
    response_format = request.POST.get('response_format')
    # Get the hashtag from the request
    hashtag = request.POST.get('hashtag')
    # Search Twitter for the hashtag
    tweets = api.search_tweets(q='#' + hashtag, lang='en', count=100, tweet_mode='extended')
    # Extract the text from the tweets
    tweet_texts = [tweet.full_text for tweet in tweets]
    # Remove URLs, hashtags, and mentions from the tweet text
    cleaned_tweet_texts = [re.sub(r'(https?://\S+|#\S+|@\S+)', '', tweet) for tweet in tweet_texts]
    # Tokenize the tweet text
    words = []
    for tweet in cleaned_tweet_texts:
        words += tweet.split()
    # Get the word frequencies
    word_frequencies = {}
    for word in words:
        if word in word_frequencies:
            word_frequencies[word] += 1
        else:
            word_frequencies[word] = 1
    # Sort the word frequencies in descending order
    sorted_word_frequencies = sorted(word_frequencies.items(), key=lambda x: x[1], reverse=True)
    # Get the top n words
    top_words = sorted_word_frequencies[:num_words]
    # Get the timestamp of the first tweet
    first_tweet_timestamp = tweets[-1].created_at
    # Get the timestamp of the last tweet
    last_tweet_timestamp = tweets[0].created_at
    # Build the response
    response = {
        'topic': hashtag,
        'timestamp_first_tweet': first_tweet_timestamp,
        'timestamp_last_tweet': last_tweet_timestamp,
        'word_cloud': top_words
    }
    # Save the data to the database
    save_data(hashtag, first_tweet_timestamp, last_tweet_timestamp, top_words)
    # Return the response in the requested format
    if response_format == 'json':
        return JsonResponse(response)
    elif response_format == 'csv':
        # Convert the response to CSV format
        csv = to_csv(response)
        # Create the HttpResponse object with the CSV file as an attachment
        response = HttpResponse(csv, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="word_cloud.csv"'
        return response


def save_data(hashtag, first_tweet_timestamp, last_tweet_timestamp, top_words):
    # Connect to the database
    conn = sqlite3.connect('word_cloud.db')
    c = conn.cursor()
    # Create the table if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS word_clouds (
            id INTEGER PRIMARY KEY,
            hashtag TEXT,
            first_tweet_timestamp TEXT,
            last_tweet_timestamp TEXT,
            top_words TEXT
        )
    ''')
    # Insert the data into the table
    c.execute('''
        INSERT INTO word_clouds (hashtag, first_tweet_timestamp, last_tweet_timestamp, top_words)
        VALUES (?, ?, ?, ?)
    ''', (hashtag, first_tweet_timestamp, last_tweet_timestamp, json.dumps(top_words)))
    # Commit the changes and close the connection
    conn.commit()
    conn.close()


def to_csv(data):
    # Create a CSV string from the data
    csv = 'Topic,Timestamp of First Tweet,Timestamp of Last Tweet,Word,Frequency\n'
    for word, frequency in data['word_cloud']:
        csv += f'{data["topic"]},{data["timestamp_first_tweet"]},{data["timestamp_last_tweet"]},{word},{frequency}\n'
    return csv
