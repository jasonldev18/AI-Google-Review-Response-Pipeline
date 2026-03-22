from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import os
from google_auth_oauthlib.flow import InstalledAppFlow
import requests
from dotenv import load_dotenv
from google.cloud import secretmanager
import json


load_dotenv()

# Restrict permissions to only access and post google reviews
SCOPES = ['https://www.googleapis.com/auth/business.manage']

#loads access token if exist, otherwise trigger first time login
def get_credentials():

    creds = None

    # Read token.json from Secret Manager
    secret_client = secretmanager.SecretManagerServiceClient()
    name = f"projects/vast-service-484419-r9/secrets/TOKEN_JSON/versions/latest"
    response = secret_client.access_secret_version(request={"name": name})
    token_data = json.loads(response.payload.data.decode("UTF-8"))

    creds = Credentials.from_authorized_user_info(token_data)

    if creds.expired and creds.refresh_token:
        creds.refresh(Request())

        # Write refreshed token back to Secret Manager
        new_secret = secretmanager.SecretManagerServiceClient()
        parent = f"projects/vast-service-484419-r9/secrets/TOKEN_JSON"
        new_secret.add_secret_version(
            request={
                "parent": parent,
                "payload": {"data": creds.to_json().encode("UTF-8")}
            }
        )

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







