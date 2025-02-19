# **AutomateSpotify**

A Python application designed to transfer your liked YouTube videos into a Spotify playlist seamlessly. This project leverages YouTube's and Spotify's APIs to automate the curation of your music library.

## **Features**

- **YouTube Integration**
  - Fetches your liked videos from YouTube.
  - Extracts metadata such as song title and artist.

- **Spotify Integration**
  - Searches for the extracted songs on Spotify.
  - Creates and updates a playlist with the found tracks in your Spotify account.

- **Flask Web Interface**
  - Provides a user-friendly web interface for interaction.
  - Allows manual control and monitoring of the playlist creation process.

- **Robust Error Handling**
  - Implements comprehensive error handling to manage API request failures and unmatched songs.

## **Technologies Used**

- **Backend Framework:** Python
- **Web Framework:** Flask
- **APIs:** YouTube Data API, Spotify Web API
- **Libraries:** `yt-dlp` (for YouTube content extraction), `requests` (for HTTP requests), `spotipy` (Spotify API client), `python-dotenv` (for environment variable management)
- **Version Control:** Git

## **Installation**

1. **Clone the Repository:**

   ```
   git clone https://github.com/GRuizV/AutomateSpotify.git
   cd AutomateSpotify

2. **Clone the Repository:**

   ```
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate

3. **Install Dependencies:**

   ```
   pip install -r requirements.txt

4. **Configure Environment Variables:**
    
    Create a .env file in the root directory with the following content:

        ```
        SPOTIPY_CLIENT_ID=your_spotify_client_id
        SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
        SPOTIPY_REDIRECT_URI=your_redirect_uri
        YOUTUBE_API_KEY=your_youtube_api_key

Replace `your_spotify_client_id`, `your_spotify_client_secret`, `your_redirect_uri`, and `your_youtube_api_key` with your actual API credentials.

5. **Run the Application:**
    
    ```
    python main.py

Access the web interface by navigating to `http://127.0.0.1:5000/` in your browser.

## **Usage**

**Configure Environment Variables:**
    
1. **Authentication:**
    - Upon running the application, authenticate with your Spotify account to grant the necessary permissions.
    
2. **Fetching Liked Videos:**
    - The application will retrieve your liked videos from YouTube and extract the relevant song information.
    
3. **Creating Spotify Playlist:**
    - The extracted songs will be searched on Spotify, and a new playlist will be created or updated with the found tracks.
    
4. **Monitoring:**
    - Use the Flask web interface to monitor the process, view logs, and manage the playlist creation.


## **Future Enhancements**

- **Automated Scheduling:** Implement a scheduling feature to update the Spotify playlist periodically without manual intervention.

- **Enhanced Matching Algorithm:** Improve the song matching algorithm to increase accuracy, considering factors like song duration and popularity.

- **User Preferences:** Allow users to set preferences for playlist naming conventions, privacy settings, and more.


## **Contributing**

- Contributions are welcome! Please fork the repository and submit a pull request with your proposed changes.


## **License**

This project is licensed under the MIT License. See the LICENSE file for details.
    







