import requests
import json

# Configuration des API
API_KEYS = {
    "twitter": {
        "bearer_token": "your_twitter_bearer_token"
    },
    "facebook": {
        "access_token": "your_facebook_access_token"
    },
    "linkedin": {
        "access_token": "your_linkedin_access_token"
    },
    "reddit": {
        "client_id": "your_reddit_client_id",
        "client_secret": "your_reddit_client_secret",
        "username": "your_reddit_username",
        "password": "your_reddit_password",
        "user_agent": "your_reddit_user_agent"
    }
}

# Exemple de contenu à publier
content = {
    "twitter": "Hello Twitter! This is an automated post from Saadiya AI.",
    "facebook": "Hello Facebook! This is an automated post from Saadiya AI.",
    "linkedin": "Hello LinkedIn! This is an automated post from Saadiya AI.",
    "reddit": {
        "title": "Automated Post from Saadiya AI",
        "selftext": "This is an automated post to the subreddit!",
        "subreddit": "your_subreddit"
    }
}

def post_to_twitter(content):
    url = "https://api.twitter.com/2/tweets"
    headers = {
        "Authorization": f"Bearer {API_KEYS['twitter']['bearer_token']}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, json={"text": content})
    return response.json()

def post_to_facebook(content):
    url = f"https://graph.facebook.com/v10.0/me/feed"
    params = {
        "message": content,
        "access_token": API_KEYS['facebook']['access_token']
    }
    response = requests.post(url, params=params)
    return response.json()

def post_to_linkedin(content):
    url = "https://api.linkedin.com/v2/ugcPosts"
    headers = {
        "Authorization": f"Bearer {API_KEYS['linkedin']['access_token']}",
        "Content-Type": "application/json"
    }
    data = {
        "author": "urn:li:person:your_person_id",  # Remplacez par votre ID LinkedIn
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": content
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

def post_to_reddit(content):
    url = "https://www.reddit.com/api/submit"
    auth = requests.auth.HTTPBasicAuth(API_KEYS['reddit']['client_id'], API_KEYS['reddit']['client_secret'])
    data = {
        "title": content['title'],
        "selftext": content['selftext'],
        "subreddit": content['subreddit'],
        "kind": "self"
    }
    headers = {"User-Agent": API_KEYS['reddit']['user_agent']}
    response = requests.post(url, auth=auth, data=data, headers=headers)
    return response.json()

def main():
    print("Posting to Twitter...")
    twitter_response = post_to_twitter(content["twitter"])
    print("Twitter response:", twitter_response)

    print("Posting to Facebook...")
    facebook_response = post_to_facebook(content["facebook"])
    print("Facebook response:", facebook_response)

    print("Posting to LinkedIn...")
    linkedin_response = post_to_linkedin(content["linkedin"])
    print("LinkedIn response:", linkedin_response)

    print("Posting to Reddit...")
    reddit_response = post_to_reddit(content["reddit"])
    print("Reddit response:", reddit_response)

if __name__ == "__main__":
    main()
    