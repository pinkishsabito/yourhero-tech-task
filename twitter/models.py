from django.db import models


class WordCloud(models.Model):
    hashtag = models.CharField(max_length=50)
    first_tweet_timestamp = models.DateTimeField()
    last_tweet_timestamp = models.DateTimeField()
    word_cloud = models.TextField()
    objects = models.Manager()
