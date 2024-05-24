import json
import spotify_helper
import CreatePlaylistHelper
from datetime import datetime


# CONSTANTS
SPOTIFY_TOKENS_JSON_FILE_PATH = spotify_helper.SPOTIFY_TOKENS_JSON_FILE_PATH


# MESSAGE VARIABLES
now = datetime.now()
timestamp = now.strftime("%d/%m/%Y %H:%M:%S")


# First contact
greeting_response = input(f'[{timestamp}] - Hello, there! Is this your first time using the app or did you revoke authorization from spotify priorly? (Y/N)\n').upper()

# Input handling
while greeting_response not in ('Y', 'N'):
    print(f'\n[{timestamp}] - Sorry, invalid answer...')
    greeting_response = input(f'\n[{timestamp}] - Is this your first time using the app or did you revoke authorization from spotify priorly? (Y/N)\n').upper()




# If authorization is needed
if greeting_response == 'Y':    

    code = spotify_helper.SpotifyHelper.authorize()
    token, refresh_token = spotify_helper.SpotifyHelper.get_token(code=code)

    print(f'''\n[{timestamp}] - Great! Apparently we got everything we need to continue...''')
    

# If authorization is not needed
else:
    
    try:
        # Consult the spotify token in the JSON file
        with open(SPOTIFY_TOKENS_JSON_FILE_PATH) as f:
            data = json.load(f)
            token = data['access_token']

            if token is None:
                print(f'\n[{timestamp}] - Oops!')
                raise Exception('''No token was found, please go back and authorize the app (reset the app and answer 'Y' to the first question)''')

            else:
                # Check if the current token is still valid
                token = spotify_helper.SpotifyHelper.request_token()
                print(f'''\n[{timestamp}] - Great! Apparently we got everything we need to continue...\n''')


    except Exception:
        raise Exception('''No authorization credentials found, please reset the app and answer 'Y' to the first question''')

# Execute the actual Bukola app

print(f'''\n[{timestamp}] - Before getting the app to work, please pay attention to the command line since if you haven't authorize the app in the Google API 
to access to your youtube playlist and likes videos, it will prompt a url to authorize it and the app will stop until you do...\n''')


# Call for the app to start its process
CreatePlaylistHelper.CreatePlaylist.add_song_to_playlist()












