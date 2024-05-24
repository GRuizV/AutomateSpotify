import os
import json, requests, base64
from dotenv import load_dotenv
from datetime import datetime, timedelta


# Loading environmental variables which include clients secrets
load_dotenv()


# CONSTANTS
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = 'http://localhost:5000/callback'
SPOTIFY_AUTH_SCOPE = 'playlist-read-private%20playlist-modify-private%20playlist-modify-public' # This scope may vary depending on what will you use the app for, but this setting allows read and modify the user's playlist which is common use case
SPOTIFY_TOKENS_JSON_FILE_PATH = r'C:\Users\USUARIO\GR\Software Development\Projects\Bukola Automate Spotify Project (2020) - Updated [2024]\spotify_tokens.json'


#MESSAGE VARIABLES
now = datetime.now()
timestamp = now.strftime("%d/%m/%Y %H:%M:%S")


# The class definition (Any operation with spotify will be handled here)
class SpotifyHelper:

    @staticmethod   
    def authorize() -> str:

        '''This function collects the authorization code from the flask server when the user gives its approval'''        


        # Ask the user to authenticate the app to Spotify (Having the flask server running)
        print(f'''\n[{timestamp}] - Alright, so in order for us to manage your playlists, the first thing we need is to get an authorization code from Spotify,
    and to do so, one necessary step is to have the flask_app (server) running* because it will receive the code.
              
            *To start the server, while still running the app, execute the 'flask_app.py' file.
         
    Now, with the server up and running, please go to the link below and authorize the access for this app into your Spotify Account

    Link: https://accounts.spotify.com/authorize?client_id={SPOTIFY_CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={SPOTIFY_AUTH_SCOPE}\n''')


        confirmation_response = input(f'''[{timestamp}] - Let us know when you completed the authorization process by typing any key or typing 'exit' to close the app: ''').casefold()


        # In case the user wants to finish the execution
        if confirmation_response == 'exit':
            print(f'\n[{timestamp}] - Closing down... (Remember to shut down the server!)')


        # In case the user wants to continue
        else:
            with open(SPOTIFY_TOKENS_JSON_FILE_PATH) as f:
              
                data = json.load(f)
                code = data['code']
                
                if code is not None:

                    print(f'\n[{timestamp}] - Fantastic! we got the code, now we can proceed...\n')
                    return code

                else:
                    print(f'\n[{timestamp}] - Oops!')
                    raise Exception(f'''\n  ERROR: Apparently we didn't receive a code!''')




    @staticmethod   
    def get_token(code) -> tuple[str]:

        '''This function request a token just after the authorization code is received, with a token and a refresh token no further authorization is needed to work'''


        try:
            # POST Request setting
            url = 'https://accounts.spotify.com/api/token'
            headers = {'Authorization': f'Basic {base64.b64encode(f'{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}'.encode()).decode()}'}
            data = {
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': REDIRECT_URI
            }
            
            # POST request sending
            response = requests.post(url, headers=headers, data=data)
            response.raise_for_status() # Raise exception for HTTP errors
            auth_data = response.json()

            # Capture the spotify authorization credentials
            access_token = auth_data['access_token']
            refresh_token = auth_data['refresh_token']
            expiration_time = datetime.now() + timedelta(seconds=3600)
            expiration_time_str = expiration_time.isoformat()+'Z'
            
                # Open the JSON file to save the tokens
            with open(SPOTIFY_TOKENS_JSON_FILE_PATH) as f:
                data = json.load(f)

                # Save the updated tokens in the JSON file
            with open(SPOTIFY_TOKENS_JSON_FILE_PATH, 'w') as f:
                data['access_token'] = access_token
                data['refresh_token'] = refresh_token
                data['expiration_time'] = expiration_time_str
                json.dump(data, f, indent=2)

            return access_token, refresh_token
        

        except requests.exceptions.RequestException as e:
            print(f'\n[{timestamp}] - ERROR FETCHING TOKEN: {e}')
            return None, None




    @staticmethod   
    def refresh_token(refresh_token) -> tuple[str]:

        '''This function request a new token with a refresh token parameter, to keep working without having to ask for the user's authorization again'''


        try:
            # POST Request setting
            url = 'https://accounts.spotify.com/api/token'
            headers = {'Authorization': f'Basic {base64.b64encode(f'{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}'.encode()).decode()}'}
            data = {
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token
            }

            # POST request sending
            response = requests.post(url, headers=headers, data=data)
            response.raise_for_status() # Raise exception for HTTP errors
            auth_data = response.json()

            # Capture the spotify refreshed authorization credentials
            access_token = auth_data['access_token']
            refresh_token = auth_data.get('refresh_token', refresh_token)   # Note: 'refresh_token' may not always be returned in refresh token requests
            expiration_time = datetime.now() + timedelta(seconds=3600)
            expiration_time_str = expiration_time.isoformat()+'Z'
            
                # Open the JSON file to save the tokens
            with open(SPOTIFY_TOKENS_JSON_FILE_PATH) as f:
                data = json.load(f)

                # Save the refreshed tokens in the JSON file
            with open(SPOTIFY_TOKENS_JSON_FILE_PATH, 'w') as f:
                data['access_token'] = access_token
                data['refresh_token'] = refresh_token
                data['expiration_time'] = expiration_time_str
                json.dump(data, f, indent=2)
                
            return access_token, refresh_token
        

        except requests.exceptions.RequestException as e:
            print(f'\n[{timestamp}] - ERROR FETCHING TOKEN: {e}')
            return None, None

        


    @staticmethod   
    def request_token() -> str:

        '''
        This functions is made to retrive a new token that has at least 5 minutes validity to execute.  

            The difference with the get_token method is that get_token receives an authorization code when is just authenticated by the user
            and not always is needed to ask for authorization (only if is a first time using the app or if the authorization was revoked in Spotify), 
            and is also inefficient to call for the refresh_token method everytime an operation will be done if the current token hasn't expired yet.

            That's why this function evaluates if it worth to refresh the current token or it can be still usuful for the operation to be executed.
        '''

        # Consult the current token and it's expiracy
        with open(SPOTIFY_TOKENS_JSON_FILE_PATH) as f:
            data = json.load(f)
            token = data['access_token']
            expiration_time = datetime.fromisoformat(data['expiration_time'][:-1])  #The [:-1] is to take out the 'Z' parameter given that we are computing this time later

        # Checking if token's worth refreshing
        if expiration_time < datetime.now() + timedelta(minutes=5):
            token, refresh_token = SpotifyHelper.refresh_token(data['refresh_token'])

        return token


