---
draft: false


date: 2024-12-01

authors: 
  - ddxv

categories:
  - Updates
---

# IP Geo Tagging and first commits for iOS and Android SDKs



The past month I focused on getting a v0.0.1 of the Android SDK working. I also worked on some basic geo IP tagging and best of all we had a super talented person show up to help with iOS SDKs. 

## Android SDK

This turned out to take a bit longer than expected, but now at least there is a very basic example of how it could one day work. What we have now is just a single function that calls `app_open` event from an Android Application. The [OpenAttribution Android SDK](https://github.com/OpenAttribution/oa-android-sdk) is also live on Maven Central and can be added as a dependency to any Android project


## IP Geo Tagging

A simple IP geo tagging service was added to the `postback-api` to get the country and city of the user. This was also added to the various testing simulated data as well. Finally the `dash-frontend` was updated to show the country for the demo site as well.


## iOS SDK

This has just gotten started as well, and likely at a much more professional setup than the Android side. The code is hosted on [OpenAttribution iOS SDK](https://github.com/OpenAttribution/oa-ios-sdk). 


So just a quick update, but things are moving forward.