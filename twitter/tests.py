from django.test import TestCase
from django.urls import reverse


class WordCloudAPITestCase(TestCase):
    def test_word_cloud_api(self):
        # Send a request to the API endpoint with the correct parameters
        response = self.client.post(reverse('word_cloud'), {
            'num_words': 10,
            'response_format': 'json',
            'hashtag': 'test'
        })
        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)
        # Check that the returned data is correct
        self.assertEqual(response.json()['topic'], 'test')
        self.assertIsNotNone(response.json()['timestamp_first_tweet'])
        self.assertIsNotNone(response.json()['timestamp_last_tweet'])
        self.assertIsInstance(response.json()['word_cloud'], list)
        self.assertEqual(len(response.json()['word_cloud']), 10)

    def test_word_cloud_api_csv(self):
        # Send a request to the API endpoint with the correct parameters
        response = self.client.post(reverse('word_cloud'), {
            'num_words': 10,
            'response_format': 'csv',
            'hashtag': 'test'
        })
        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)
        # Check that the returned data is correct
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertEqual(response['Content-Disposition'], 'attachment; filename="word_cloud.csv"')
        self.assertIsInstance(response.content, bytes)

    def test_word_cloud_api_invalid_format(self):
        # Send a request to the API endpoint with an invalid response format
        response = self.client.post(reverse('word_cloud'), {
            'num_words': 10,
            'response_format': 'invalid',
            'hashtag': 'test'
        })
        # Check that the response is 400 BAD REQUEST
        self.assertEqual(response.status_code, 400)
