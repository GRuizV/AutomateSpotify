import os
import re
import json, requests
import spotify_helper
import googleapiclient.errors
import google_auth_oauthlib.flow
import googleapiclient.discovery
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from dotenv import load_dotenv
# import youtube_dl DEPRECATED!
import yt_dlp as youtube_dl




# Loading environmental variables which include clients secrets
load_dotenv()


# CONSTANTS
SPOTIFY_USER = os.getenv('SPOTIFY_USER')
YT_JSON_FILE_PATH = r'C:\Users\USUARIO\GR\Software Development\Projects\Bukola Automate Spotify Project (2020) - Updated [2024]\Bukola YT PJ\youtube_client_secrets.json'
PROJECTS_PATH = r'C:\Users\USUARIO\GR\Software Development\Projects\Bukola Automate Spotify Project (2020) - Updated [2024]'




class CreatePlaylist:
    

    # Step 1: Log into Youtube
    @staticmethod
    def get_youtube_client() -> googleapiclient.discovery.build:

        '''This function authenticates the user using OAuth 2.0 and returns a service object for the YouTube API.'''

        # This part of the code was taken from the Youtube API Documentation
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"
        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = YT_JSON_FILE_PATH
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]


        # Load credentials from file if available
        tokens_file_path = os.path.join(PROJECTS_PATH, 'youtube_tokens.json')
        creds = None

        # In case the credentials exist
        if os.path.exists(tokens_file_path):
            creds = Credentials.from_authorized_user_file(tokens_file_path)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            
            # If a token refreshing is needed
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())

            # If authorizing is needed (Could be that is the first time using it or the refreshing is not able to do its work)
            else:
                flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
                creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open(tokens_file_path, 'w') as token:
                token.write(creds.to_json())


        # Build the youtube service
        youtube_client = googleapiclient.discovery.build(api_service_name, api_version, credentials=creds)

        return youtube_client
    


    
    # Step 2: Grab Liked Videos
    # Originally this method used youtube_dl but since deprecation, yt_dlp is used instead but with the same name (youtube_dl)
    @staticmethod
    def get_liked_videos() -> list:
        
        ''' This function will receive a youtube service comming from the get_youtube_client function and will return a dict with the relevant data of the liked videos '''

        # Create the new youtube service
        youtube_client = CreatePlaylist.get_youtube_client()

        # Build the request
        request = youtube_client.videos().list(part="snippet,contentDetails,statistics", myRating = "like")

        # Send the request to the Youtube API
        response = request.execute()

        # This dict will store the output
        all_song_info = []

        # Collect the relevant data from each video
        for item in response["items"]:

            video_title = item["snippet"]["title"]
            youtube_url = f'https://www.youtube.com/watch?v={item["id"]}'

            # Use yt_dlp as youtube_dl to collect info to later deduce artist's and track's names
            video = youtube_dl.YoutubeDL({}).extract_info(youtube_url, download=False)

            # Store the relevant info in the dict
            all_song_info.append((video['uploader'], video_title))  # The 'updloader' in the yt_dlp response commonly coincides with the actual artist name


        # PARSING THE VIDEO TITLE TO DEDUCE THE SONG'S NAME

        # Here will be held the final (artist name, track name) for the youtube response
        songs = []

        # Regular expression pattern
        pattern = re.compile(r'^(.+?)\s*-\s*(.+?)\s*[\(|\|].*') # this regex means "Match anything from the begning to the hyphen, and everything else from the hypen to the next '(' or '|'"

        # Extractng song names
        for artist, title in all_song_info:

            match = pattern.match(title)
            elem1, elem2 = None, None   # Initialize the names holder

            # Catch the names (we don't know which is artist and which is name)
            if match:
                elem1 = match.group(1)
                elem2 = match.group(2)
        
            # In case it matches with anything
            if elem1 and elem2:

                art_name = artist.split()[0].casefold() # the 0 index is because sometimes the artist has a composed name
                
                # If the elem1 has the artist name in it, it'd mean the elem2 is the track's name and viceversa
                if art_name in elem1.casefold():
                    songs.append((artist, elem2, CreatePlaylist.get_spotify_uri(song_name=elem2, artist=artist)))   # The output will be in the from (artist_name, song_name, corresponding_spotify_uri)
                else:
                    songs.append((artist, elem1, CreatePlaylist.get_spotify_uri(song_name=elem2, artist=artist)))

        return songs




    # Step 3: Create a New Playlist
    @staticmethod
    def create_playlist() -> str:
        
        '''This function creates a new playlist and returns the new Playlist ID'''

        # POST Request setting
        details = {
            "name" : "Youtube Liked Vids",
            "description" : "All Youtube Liked Videos Songs",
            "public" : True
        }
        
        query = f"https://api.spotify.com/v1/users/{SPOTIFY_USER}/playlists"

            # Access token requesting
        token = spotify_helper.SpotifyHelper.request_token()

        headers = {
            "Content-Type" : "application/json",
            "Authorization" : f"Bearer {token}"
        }

        # Send the POST Request
        try:            
            response = requests.post(url=query, data=json.dumps(details), headers=headers)
            response.raise_for_status()
            response_json = response.json()            

            # Return the ID of the newly created playlist
            return response_json['id']


        except Exception as e:
            print(e)
            return None
    
    


    # Step 4: Search for the Song
    @staticmethod
    def get_spotify_uri(song_name:str, artist:str) -> str:

        '''This function retrieves the ID of a searched track'''

        # GET Request setting
        # Input treatment
        song_name = song_name.replace(' ','%2520')
        artist = artist.replace(' ','%2520')

        # Example query: (Cicuta - Noiseferatu) 'https://api.spotify.com/v1/search?q=remaster%2520track%3Acicuta%2520artist%3Anoisefaratu&type=track&market=CO&offset=0'
        query = f'https://api.spotify.com/v1/search?q=remaster%2520track%3A{song_name}%2520artist%3A{artist}&type=track&market=CO&offset=0'
        
        # Get the Access Token
        token = spotify_helper.SpotifyHelper.request_token()

        # Build the 'headers'
        headers = { 
            "Content-Type" : "application/json",
            "Authorization" : f"Bearer {token}"
        } 


        # Send the GET Request
        try:            
            response = requests.get(url=query, headers=headers)
            response.raise_for_status()
            response_json = response.json()            

            # this are the songs that matched the search above
            songs = response_json["tracks"]["items"]

            # ***Careful: this project only cared for the firs match / Meaning that not always the precise searched song will be added to the final playlist
            uri = songs[0]["uri"]

            return uri
        

        except Exception as e:
            print(e)
            return None



   
    # Step 5: Add the song into the new Spotify playlist
    @staticmethod
    def add_song_to_playlist() -> str:

        ''' This function executes the whole app process: returns the id of the newly created playlist'''
       
        # Collect the song's uris
        uris = [item[2] for item in CreatePlaylist.get_liked_videos()]  # Items comming from 'get_liked_videos' come in the form (artist_name, song_name, corresponding_spotify_uri) that's why I used 'item[2]'

        # Create the new playlist
        playlist_id = CreatePlaylist.create_playlist()

        # POST Request setting
        # Add all songs into new playlist
        request_data = json.dumps(uris)
        query = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'

        # Request Access Token
        token = spotify_helper.SpotifyHelper.request_token()

        # Build the 'headers'
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }

        # Send the POST Request
        try:            
            response = requests.post(url=query, data=request_data, headers=headers)
            response.raise_for_status()
            response_json = response.json()

            # Success Message
            print('\n\nThe playlist with your liked videos from Youtube was successfully created!\n\n')           


        except Exception as e:
            print(e)
            return None

