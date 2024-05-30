# Automate Spotify (2020) - Updated[2024]

## Description

This project is the update of the original Bukola's project with the same name (Below is the link to the original content). 

**Main feature**
This is a tutorial in how to build a simple Python project that can make requests to Google's and Spotify's API to bring the 'liked' videos of you favorite songs into a playlist in yur Spotify Account.

> __Please Note!:__ that this update was made due to the original tutorial recommended the use of youtube_dl's library but apparently was deprecated since 2022 due to legal issues.

Given that 'youtube_dl' is absolutely necessary for the app to function, to keep the project running another library ('yt-dlp') was used as replacement. The main function of this library is to try to retrive the track's and artist's names to later make a search in spotify to add it to our 'Youtube Liked' songs.


### Regarding the APIs

The most challenging part of this project (from a beginner's POV) is the Authorization process in both APIs. Given that you are going to access to "someone's" Youtube and Spotify account information (i.e.: Liked videos, spotify profile and playlist) you will need to understand how those process goes, both based on OAUTH2.0, so my recommendation is to go an get familiar with both APIs, how they receives requests, how they answer and how to make the HTTP calls to their respective endpoints.

> __Please also be aware:__ A lot have changed since 2020, now both Google and Spotify have some different requirements on how to validate an app that make calls to their APIs' endpoints, so please be sure you understand those processes before attempting to follow Bukola's original tutorial right away.

>> For instance, the way to get a Token from Spotify is not just to take it from the Spotify dashboard (As Bukola does in her tutorial), now is required to authorize by going through a page and having a server receiving HTTP responses and await for a 'code' back to trade it for a token (That's why this project is not a single file project like the original).


### Regarding this project files

**_Folders_**

- **JSON Objects Structure:** jnflnds

- **Youtube_dl replacement:** jnflnds

- **ref imgs:** jnflnds


**_Main files_**

- **requirements.txt**: This file contains all the dependencies you need for this app.

- **.gitignore**: dsfsdf.

- **CreatePlaylistHelper.py**: dsfsdf.

- **flask_app.py**: dsfsdf.

- **spotify_helper.py**: dsfsdf.

- **main.py**: dsfsdf.

- **test_suite.py**: dsfsdf.


**_Auxiliary files_**

> _Please Note:_ That the Auxiliary files are not being tracked since they contain sensitive information, so be sure your project's directory contains them with the same name, otherwise the app won't execute.

- **youtube_client_secrets.json**: You can get this file downloading it from Google's Cloud Console (Where you will manage your project for the Google derivated API (Youtube)), in the 'APIs & Services' link from the quick access, in the 'credentials' section of the left bar, in the link of the name of your app
    
    [Google's Cloud Console Link](https://console.cloud.google.com/)


    ![Screenshot](https://i.ibb.co/Q8R66TZ/Youtube-Client-ID-Client-Secret-ref.png)


    _Mocking data_
  
    ![Screenshot](https://i.ibb.co/C5QpwSD/youtube-client-example.png)


- **youtube_tokens.json**: This file actually populates automatically while the execution of the app, you just need to make sure it exist inside the project's directory.

- **spotify_tokens.json**: This file actually populates automatically while the execution of the app, you just need to make sure it exist inside the project's directory.

- **.env file**: This file needs to be also in the same project's directory as shown below.

    ![Screenshot](https://i.ibb.co/74y2XTP/env-example.png)


    _And here is where you get your Spotify ID from the Spotify API documentation_

    ![Screenshot](https://i.ibb.co/GWKg7p0/Spotify-user-ID-getting.png)

    The actual link for this section of the Spotify documentation is [here](https://developer.spotify.com/documentation/web-api/reference/get-current-users-profile)





## Instructions

> __IMPORTAMT!:__ The main the prerequisite for this app to work is **that the liked videos in your youtube account must be the official songs in the actual artist channel** for the app to work.

1. Make sure to install all the dependencies required (You can execute the 'pip install -r requirements.txt' being inside your project's directory)

2. ...



## Links


__Original Youtube Project Tutorial Video:__ https://www.youtube.com/watch?v=7J_qcttfnJA&list=PL0erUSr3_-uP0J-oKEyCymclK18sEk2L0

__Spotify for Developers (API Site):__ https://developer.spotify.com/

__Youtube DataAPI (API site - _This is more for understanding how to make the calls, the endpoints and else_):__ https://developers.google.com/youtube/v3

__Google for Developers (_You'll actually need to manage the Youtube part of your project here_):__ https://developers.google.com/




## Next enhancements

- Manage pagination from Youtube API response to handle more than 5 liked videos.
- Acoustic Fingerprinting to enhance the matches.

