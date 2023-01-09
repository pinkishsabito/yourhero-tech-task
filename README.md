# YourHero/Douleutaras Candidate Assessments
## Instructions
1. Create a new private repo in Gitlab with your code
2. Invite the following users: @pkallis, @gbouziotopoulos
3. Let us know you have completed the task.
## Things to avoid
- A lot of code, keep your code as simple as possible
- Copy-pasting code from other libraries
- Not asking for clarification. If something is not clear, please let us know.
**Important Note**: If you are unsure of something or require further clarification please describe and we will respond immediately.
****
# Backend Assessment Task
## Twitter Word Cloud API
### Description
Create an authenticated REST API endpoint, using your preferred Python framework, which will return a word cloud for the last 24h of any hashtag you choose from Twitter. You may choose any technology you want for storing the data.
### Requirements
The endpoint should be able to accept only authenticated requests (key, session, etc.) containing the following fields:
- The maximum number of words to return
- Whether the response should be JSON or CSV formatted

The response should contain the following fields in the format requested:
- The information related to the number of words requested
- The topic
- The timestamp of the first tweet
- The timestamp of the last tweet
Also, please try to include any relevant unit test and code comments with your work.
### Delivery
It would be good if the code is accompanied by a 1-page report of the work you have done.
Please, do not spend more than an afternoon on this task! It is just a basis to allow a technical interview and a pleasant tech discussion!
****
## About
### Main Code located inside of files below
- twitter/models.py
-  twitter/tests.py
-  twitter/urls.py
-  twitter/views.py
