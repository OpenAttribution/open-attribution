# Background on Attribution

Attribution is the process of marking where a user came from for advertising purposes. In digital you might have a link like:

```https://ecommercesite.com/products/productA?referral=MyAdCampaign```

The above link hands off information about where the user came from to the destination. Thus if a person makes a purchase this can be attributed back to the source.

Attribution exists as a problem for mobile developers and advertisers because they do not have the same capabilities as web to use HTTP urls. When a user clicks a URL for the PlayStore that data can contain a referral but this information only goes to Google Play Store itself. Each user downloads the same app as each other. For security, there is no information from that URL inserted into the downloaded package. At this point the information in the URL is lost and thus not usable in the app when it opens for any kind of postback.

### Device identification: IMEI -> IDFA -> Fingerprinting

To get around the lack of HTTP URL data advertisers used identifiers like IMEI and UDID. These IDs presented a very concrete way of identifing devices across any app and presented much more capabilities than what would usually be pased in a URL. To combat this privacy concern the IFA/IDFA and Advertising IDs were introduced around 2012 by Apple and later Google.

These IDs only partially solved all privacy concerns as they still allowed any apps to match users without any explicit concent from the user.

In 2020 Apple decided to completely remove support for IDFA. Apps, still without the ability to use HTTP URLs to link where a user came from resorted to HTTP links.

## Q: So without URLs, how can one app know it's link to another? A: MMPs

MMPs like AppsFlyer, Branch and Adjust help advertisers recreate the HTTP URL by using using device identificaiton to attribute a user from a click to a later app open.

For our example lets say there are two apps: A social media platform and a indie game. The game sets up two campaigns on the social media platform, and wants to see which one converts users best.

In order for the game to know which campaign works best They use an MMP which collects two separate streams of information and performs attribution. Each app will query the operating system to find out that devices ifa and fill it in the link for `{ifa}`.

On the social media platform the click link:

`mmp.com/com.mygame?campaign=MyCampaign&ifa={ifa}`

From within the game when it is opened for the first time:

`mmp.com/com.mygame?event=app_open&ifa={ifa}`

Then the MMP would do lookback to see which click has the same matching IFA.

The problem here is that the MMP to do the matching requires both sets of data and thus has the most access to both the social media app and game's data. In the past this was a small price to pay for what was essentially impossible to do without the MMP.

## Enter Open Attribution

Open Attribution is here to empower a developer to keep ownership of their sensitive business data. Open Attribution gives the tools an MMP uses directly to the app so that they can manage their own advertising data without the need for a 3rd party.

### Open Attribution gives developers their data back

Using open attribution allows a developer to host their own MMP so that their campaign and sensitive data is not shared with another company. 

