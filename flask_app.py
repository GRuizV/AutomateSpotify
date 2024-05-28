import flask, json
import spotify_helper


# CONSTANTS
SPOTIFY_TOKENS_JSON_FILE_PATH = spotify_helper.SPOTIFY_TOKENS_JSON_FILE_PATH
SPOTIFY_CLIENT_ID = spotify_helper.SPOTIFY_CLIENT_ID
REDIRECT_URI = spotify_helper.REDIRECT_URI
SPOTIFY_AUTH_SCOPE = spotify_helper.SPOTIFY_AUTH_SCOPE


# Flask app setting
app = flask.Flask(__name__)


# Home page definition
@app.route('/')
def home():
    
    # Spotify authorization URL
    auth_url = f'https://accounts.spotify.com/authorize?client_id={SPOTIFY_CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={SPOTIFY_AUTH_SCOPE}'
    
    # HTML content with embedded URL
    html_content = f"""
    <html>
    <body>
    <h1>Welcome to the Spotify Playlist Manager!</h1>
    <p>Please authorize the app by visiting the following Link:</p>
    <a href="{auth_url}">Link</a>
    </body>
    </html>
    """
    return html_content


# Callback page definition
@app.route('/callback')
def callback():

    # GET Request to retrive the authorization code returned by spotify
    code = flask.request.args.get('code')

    # if a code is received in the server
    if code:

        try:
            # Try to open the JSON file to read the existing tokens
            with open(SPOTIFY_TOKENS_JSON_FILE_PATH, 'r') as f:
                data = json.load(f)

        except json.JSONDecodeError:
            # if the file doesn't exist, create an empty data dictionary
            data = {}

        # Update the data dictionary with the code received
        data['code'] = code

        # Store the code in the JSON file
        with open(SPOTIFY_TOKENS_JSON_FILE_PATH, 'w') as f:
            json.dump(data, f, indent=2)

        # Redirect to a success page
        return flask.redirect('/sucess')
    

    else:
        # Handle the case where the code is missing
        return 'Authorization code missing', 400


# Success page definition
@app.route('/sucess')
def sucess():
    return f'<h1> Authorization successful! Now you can start to modify your playlists.</h1>'




if __name__ == '__main__':

    app.run(port=5000)
