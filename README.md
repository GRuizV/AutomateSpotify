# Automate Spotify (2020) - Updated[2024]

## Description

This project is the update of the original Bukola's project with the same name (Below is the link to the original content). 

**Main feature:** This is a tutorial in how to build a simple Python project that can make requests to Google's and Spotify's API to bring the 'liked' videos of you favorite songs into a playlist in your Spotify Account.

> __Please Note!:__ that this update was made due to the original tutorial recommended the use of youtube_dl's library but apparently was deprecated since 2022 due to legal issues.

Given that 'youtube_dl' is absolutely necessary for the app to function, to keep the project running another library ('yt-dlp') was used as replacement. The main function of this library is to try to retrieve the track's and artist's names to later make a search in spotify to add the result to our Youtube 'Liked' songs new playlist.

### Prerequisites

- Have a valid spotify account.
- Have a valid google account (With a youtube profile with at least one liked video from an official artist channel _later will be explained why it is important_).
- Python 3.12.
- Python libraries in the requirements file installed.

### Regarding the APIs

The most challenging part of this project (from a beginner's POV) is the Authorization process in both APIs. Given that you are going to access to "someone's" Youtube and Spotify account information (i.e.: Liked videos, spotify profile and playlist) you will need to understand how those process go, both based on OAUTH2.0, so my recommendation is to go and get familiar with both APIs, how they receives requests, how they answer and how to make the HTTP calls to their respective endpoints.

> __Please also be aware:__ A lot have changed since 2020, now both Google and Spotify have some different requirements on how to validate an app that make calls to their APIs' endpoints, so please be sure you understand those processes before attempting to follow Bukola's original tutorial right away.

>> For instance, the way to get a Token from Spotify is not just to take it from the Spotify dashboard (As Bukola does in her tutorial), now is required to authorize by going through a page and having a server receiving HTTP responses and await for a 'code' back to trade it for a token (That's why this project is not a single file project like the original).

### Regarding this project files

**_Folders_**

- **JSON Objects Structure:** This folder serves a reference on how the different APIs and endpoints return the calls. It contains the structure of a Spotify playlist response, a Spotify song search response and Youtube's liked videos response. _The intention of this part of the project was to know specifically what may be useful within the App to pull from the JSON response in each of those cases_.

- **Youtube_dl replacement:** Here are experiments with yt-dlp and youtube_title_parse modules to test which could be more useful as replacement for the youtube-dl library.

- **ref imgs:** Here are the support images for this readme file.

**_Main files_**

- **requirements.txt**: This file contains all the dependencies you need for this app.

- **main.py**: This file's just the entry point and serves to guide the first contact and from the app will be executed. _This was made to make sure one fundamental step is made when either the app is being used for the first time or the permission to access to the user's spotify private info was revoked, by prompting the user to turn on (execute in parallel) the flask server, since there is where the first authorization code will be received._

- **spotify_helper.py**: This module handles the authorization functions with spotify, such as first authorization, first token request and token refreshing. _I'd do more sense to have all spotify related functions in here but I wanted to keep the CreatePlaylistHelper as similar to what the original project was to maintain certain familiarity with that project._

- **flask_app.py**: This file simply creates a very basic flask server that while turned on will be receiving responses from spotify app authentication endpoint. 

    > The intention of this file is only when is the first time or re authorization of the app in spotify is the case and is intended to be executed **while** the main file is also being executed because it will receives the authorization code and update it into the supporting spotify_tokes.json file.

- **CreatePlaylistHelper.py**: This module contains the same five functions Bukola created in the original tutorial with some modifications to still work as the original project did.

- **test_suite.py**: This file was made to individually test functions or parts of functions.

**_Auxiliary files_**

> _Please Note:_ That the Auxiliary files are not being tracked since they contain sensitive information, so be sure your project's directory contains them with the same name, otherwise the app won't execute.

- **youtube_client_secrets.json**: You can get this file downloading it from Google's Cloud Console (Where you will manage your project for the Google derived API (Youtube)), in the 'APIs & Services' link from the quick access, in the 'credentials' section of the left bar, in the link of the name of your app
    
    [Google's Cloud Console Link](https://console.cloud.google.com/)

    ![Screenshot](https://i.ibb.co/Q8R66TZ/Youtube-Client-ID-Client-Secret-ref.png)

    _Mocking data_
  
    ![Screenshot](https://i.ibb.co/C5QpwSD/youtube-client-example.png)

- **youtube_tokens.json**: This file actually populates automatically while the execution of the app, you just need to make sure it exist as an empty JSON file inside the project's directory.

- **spotify_tokens.json**: This file actually populates automatically while the execution of the app, you just need to make sure it exist as an empty JSON file inside the project's directory.

- **.env file**: This file also needs to be in the same project's directory as shown below.

    ![Screenshot](https://i.ibb.co/74y2XTP/env-example.png)

    _And here is where you get your Spotify ID from the Spotify API documentation_

    ![Screenshot](https://i.ibb.co/GWKg7p0/Spotify-user-ID-getting.png)

    The actual link for this section of the Spotify documentation is [here](https://developer.spotify.com/documentation/web-api/reference/get-current-users-profile)




## Instructions

__IMPORTANT!:__ The main the prerequisite for this app to work is **that the liked videos in your youtube account must be the official songs in the actual artist channel** for the app to work.

> This was due to the difficulty to parse the track's and artist's names from the title of the videos. The project originally assumed that youtube_dl library handles that part but since it was not longer an option, I opted for using something similar and support the parsing with ruling that the track's and artist's name will follow some common naming pattern in official music videos. _The common naming convention assumed here was:_ "element_1 - element2 '| or (' Official Song". 
>
> Please consider that this project is more intended to be used in learning how APIs work and to have it as a challenge or guide in to do so than into actually matching songs from Youtube to Spotify. If that should be case, certainly must be better ways to make this matches.

1. Make sure to install all the dependencies required. _You can execute the 'pip install -r requirements.txt' being inside your project's directory_

2. Open the _main.py_ file and execute it.

3. Answer 'Y' to the question asked in the command line. _If is the first time using the app or if you revoked from spotify the authorization for the app to access your info, otherwise you could just answer 'N'_.

4. The app will wait until you open the Flask server* and with both files running you go to the link prompted in the console and authorize the app with your spotify account. _the link will send you to a spotify's authentication site in which your spotify account open you must grant access by clicking the 'Accept' button_.

>If everything goes well, you will be redirected to a page with a message saying that the Authorization was successful.
>
>*Flask server turning on: being in the 'flask_app.py' as 'main.py' is running, you must execute another instance of python for this file (if you are on VSCode, you can do this by pressing Ctrl+F5, VSCode will ask if you want to create another python instance to which you must reply with 'Yes').

5. Now that you have an authorization code received and saved in the 'spotify_tokens.json' file, you can respond in console with anything but 'exit' to continue.

6. Now, if you haven't used the app before, that means you haven't authorized the app with google since it will be making calls requesting your liked videos info, so the app will redirect your in your opened browser to an authorization process similar to spotify's, but for this the flask server is not needed, you just to go authorize in the browser the app to continue

7. With the permission granted, now you will start to see messages from the app fetching info from your liked videos and after a little while it will finish and show a message informing that the playlist is now created.

**Final note:** I am assuming here that all the needed setting for you app to work with google's cloud console is already managed, so please make sure you understand how you create a project, how you assign roles and grants permission for users to use the app. It is not something hard to do but if you haven't worked with it before it takes a moment to get the flow how the project management in google's API. 

>This app as it is only can manage up to 5 liked videos from youtube since no youtube’s response pagination handling was included, that will be left for future enhancements.

## Links

__Original Youtube Project Tutorial Video:__ https://www.youtube.com/watch?v=7J_qcttfnJA&list=PL0erUSr3_-uP0J-oKEyCymclK18sEk2L0

__Spotify for Developers (API Site):__ https://developer.spotify.com/

__Youtube DataAPI (API site - _This is more for understanding how to make the calls, the endpoints and else_):__ https://developers.google.com/youtube/v3

__Google for Developers (_You'll actually need to manage the Youtube part of your project here_):__ https://developers.google.com/



## Next enhancements

- Manage pagination from Youtube API response to handle more than 5 liked videos.
- Acoustic Fingerprinting to enhance the matches.


