import tweepy

# Remplacez ces valeurs par vos propres informations d'identification API Twitter
API_KEY = 'your_api_key'
API_SECRET_KEY = 'your_api_secret_key'
ACCESS_TOKEN = 'your_access_token'
ACCESS_TOKEN_SECRET = 'your_access_token_secret'

# Authentification
auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

# Publier un tweet
tweet_content = "Découvrez notre logiciel Saadiya ! Automatisez votre marketing digital dès aujourd'hui."
api.update_status(tweet_content)
print("Tweet publié avec succès!")
