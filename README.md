# Automate Spotify (2020) - Updated[2024]

## Description

This project is the update of the original Bukola's project with the same name (Below is the link to the original content). 

This is a tutorial in how to build a simple Python project that can make requests to Google's and Spotify's API to bring the 'liked' videos of you favorite songs into a playlist in yur Spotify Account.

> __Please Note!:__ that this update was made due to the original tutorial recommended the use of youtube_dl's library but apparently was deprecated since 2022 due to some legal issues.

As countermeasure to keep the project functioning another library was used called 'yt-dlp' which function pretty similar to the original youtube_dl. The main function of this library is to try to retrives the track's and artist's names to later make a search in spotify to add it to our 'Youtube Liked' songs.


### Regarding the APIs

The most challenging part of this project (from a beginner's POV) is the Authorization process in both APIs. Given that you are going to access to "someone's" Youtube and Spotify account information (i.e.: Liked videos, spotify profile and playlist) you will need to understand how those process goes, both based on OAUTH2.0, so my recommendation is to go an get familiar with both API's, how they receives requests, how they answerd and how to actually make the HTTP calls.

> __Please also be aware:__ That a lot of thing changed since 2020, and now both Google and Spotify have some different requirements on how to validate an app that will be make call to their APIs, so please be sure you understand those processes before attempting to follow Bukola's original tutorial right away.

>> For instance, the way to get a Token from Spotify is not just to take it from the Spotify dashboard, now is required to authorize by going through a page and having a server receiving HTTP responses to the a 'code' back and trade it for a token (That's why this project is not a single file project like the original)


### Regarding this project files





### Links
__Original Youtube Project Tutorial Video:__ https://www.youtube.com/watch?v=7J_qcttfnJA&list=PL0erUSr3_-uP0J-oKEyCymclK18sEk2L0

__Spotify for Developers (API Site):__ https://developer.spotify.com/

__Youtube DataAPI (API site - _This is more for understanding how to make the calls, the endpoints and else_):__ https://developers.google.com/youtube/v3

__Google for Developers (_You'll actually need to manage the Youtube part of your project here_):__ https://developers.google.com/