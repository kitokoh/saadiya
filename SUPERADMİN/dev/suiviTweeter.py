import tweepy

# Identifiants API Twitter
API_KEY = 'your_api_key'
API_SECRET = 'your_api_secret'
ACCESS_TOKEN = 'your_access_token'
ACCESS_TOKEN_SECRET = 'your_access_token_secret'

# Authentification et recherche de mentions
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Rechercher des mentions
mentions = api.search_tweets(q="your_software_name", count=10)
for mention in mentions:
    print(f"{mention.user.screen_name}: {mention.text}")
