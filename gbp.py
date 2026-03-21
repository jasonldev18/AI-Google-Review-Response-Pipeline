from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import os
from google_auth_oauthlib.flow import InstalledAppFlow
import requests
from dotenv import load_dotenv



load_dotenv()

# Restrict permissions to only access and post google reviews
SCOPES = ['https://www.googleapis.com/auth/business.manage']

#loads access token if exist, otherwise trigger first time login
def get_credentials():

    creds = None

    #If access token is expired and refresh token exists, request for new access token and rewrite token.json with the new tokens
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')
    
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())

            with open('token.json', 'w') as f:
                f.write(creds.to_json())
    
    else:

        #initializes flow by reading credentials and specifying scope
        #runs local server to get user credentials
        flow = InstalledAppFlow.from_client_secrets_file('client_secrets.json', SCOPES)
        creds = flow.run_local_server(port=0)
        
        with open('token.json', 'w') as f:
            f.write(creds.to_json())


    return creds



def fetch_reviews():

    creds = get_credentials()
    accountId = os.getenv('GBP_ACCOUNT_ID')
    locationId = os.getenv('GBP_LOCATION_ID')

    headers = {
        'Authorization': f'Bearer {creds.token}'
    }

    review = requests.get(
        f'https://mybusiness.googleapis.com/v4/accounts/{accountId}/locations/{locationId}/reviews',
        headers=headers
    )

    response = review.json()
    return response['reviews']



def post_response(review_id, response_text):

    creds = get_credentials()
    accountId = os.getenv('GBP_ACCOUNT_ID')
    locationId = os.getenv('GBP_LOCATION_ID')

    headers = {
            'Authorization': f'Bearer {creds.token}'
    }

    review = requests.put(
        f'https://mybusiness.googleapis.com/v4/accounts/{accountId}/locations/{locationId}/reviews/{review_id}/reply',
        headers=headers,
        json={'comment': response_text}
    )

    return review.status_code







