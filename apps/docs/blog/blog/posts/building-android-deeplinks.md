---
draft: false

date: 2025-01-28

authors:
  - ddxv

categories:
  - Updates
---

# Building Android SDK Deep Links

Happy 2025 and let's get started. This past week I started working on the Android deep links. The goal is to have a flexible app links which can be used for sharing, marketing and attribution.

My first hurdle for Android was that OpenAttribution will need to host the `.well-known/assetlinks.json` file. This is a requirement for Google to allow the app to be installed from a link. This meant some new forms needed to be added to the `dash-frontend` to allow for this. Since that was being done, I also did this for the iOS side and the `.well-known/apple-app-site-association` file.

## Android SDK

The Android SDK so far does not have the handling for receiving the deep link. This is because for the MVP of the deep link to open the app, we only need to adjust the `AndroidManifest.xml` file to include the corresponding intent filter which will match the data hosted in `.well-known/assetlinks.json`.

As such, for OpenAttribution, the main to do for handling the deep links is the redirect from the click link and the documentation for how to modify the `AndroidManifest.xml` file.

## Sharing the Links in other Apps

This is where I hit my biggest issue. When I shared my first go around with the apps, which were redirecting to the App Store URL, this would work in some apps like WhatsApp, but wouldn't work in many others.

This is because not all apps support the deep link protocol correctly. Supposedly, the apps should see `mysharelink.openattribution.dev` and when they launch the intent to open that link, the Android OS intercepts this as a known deep link (from AndroidManfiest) and then the app is launched.

Many apps such as Discord, FacebookMessenger etc do not support this. I think this is because those apps want to capture data about what link is being clicked, hence they have their own custom handling for the deep link protocol.

## Work Around

After several days of research and testing I finally found the solution was simply to redirect the share link to the `market://` protocol and include the `url=com.mypackage.name` parameter. This link will then be handled by the Google Play Store decding if the app is installed (open app) or not (open Google Play Store).

Oddly, I found NO documentation on this `url=` parameter, but stumbled across it while seeing how Firebase Dynamic Links worked. They use the `url=` parameter to redirect to the app store, which seems to work in all the apps I tested.

## Conclusion

I'm happy to say that the Android SDK is now working and the deep links are being handled correctly. The next step is to add the handling for the deep links in the `postback-api` and then the `dash-frontend` to show the deep link data.
