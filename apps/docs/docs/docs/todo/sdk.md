# SDKs

We currently have two SDKs, one for Android and one for iOS which will/should share their intent but not their implementation.

[iOS SDK](https://github.com/openattribution/oa-ios-sdk)
[Android SDK](https://github.com/openattribution/oa-android-sdk)

## SDK Shared Goal

To have a fully functional SDK which can be used to track and attribute installs, events and revenue for iOS back to an OpenAttribution server.

### MVP feature roadmap

- Library installable via Cocoapods (? is this the right approach?) or other dependency manager for mac/ios
- user input server endpoint ie `https://demo.openattribution.dev`
- event tracking with params
- documentation for how to use and next steps


## Current Partial Implementations of Tracking


### Event tracking and params details
Events:
- Basic app_open tracking and attributing
- Basic event tracking
- Basic revenue tracking

### ExistingOpenAttribution Params:

These are very loosely defined in:
https://github.com/OpenAttribution/Open-Attribution/blob/main/apps/postback-api/config/dimensions.py

```python
# In App key values
APP_EVENT_UID = "event_uid" # UUID4, unique per tracking call
APP_EVENT_ID = "event_id" # app_open, event_name
APP_EVENT_TIME = "event_time" # epoch timestamp in ms
APP_EVENT_REV = "revenue" # not sure if this is float or string
APP_OA_USER_ID = "oa_uid" # UUID4, unique per user
```

#### Sample postback payload
```
https://demo.openattribution.dev/collect/events/com.example.app?ifa=00000000-0000-0000-0000-000000000000&event_time=1732003510046&event_uid=5730a99e-b009-41da-9d52-1315e26941c1&event_id=app_open&oa_uid=3bd9e091-fa6e-4b91-8dd1-503f8d4fe8f2
```

## Future MVP Features

### Functional Features

- **Linking**
  - Shortened links generated on the server with hash-based payload lookup. Note: These do not work offline and can be blocked. Allow 3rd party shorteners.
  - Regular links can be generated anywhere. Large payloads may result in large URLs, which are less user-friendly but more reliable.

- **Sharing**
  - Support for sharesheets and Airdrop.
  - Payloads often consist of links.

- **Notifications**
  - Integration with 3rd party providers, as push notifications are complex.

### Ads Features

- **Data Collection**
  - For attribution and fraud analysis.

- **Events**
  - Attributable events: Install, open, purchase, etc. These incur additional server-side costs with the attribution pipeline.
  - Non-attribution events: A/B testing, usability testing. While MMPs typically avoid these, many app developers do not differentiate. Assume only install and purchase are attributable by default; other events are for developer insights.

- **Engagement History**
  - Prefer storing most data on-device.
  - Allow 3rd party analytics access.

- **Ad Network Specific Features**
  - Apple AdAttributionKit support as a separate target. Apps prefer server control over conversion values and mappings.
  - Token Collection:
    - Apple attribution token for Apple Search Ads.
    - Link query parameters for other ad networks, mainly for web-to-app transitions.