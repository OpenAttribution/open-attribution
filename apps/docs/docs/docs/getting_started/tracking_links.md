# App Integration

## App Events

Endpoint: `/collect/events/{MY-APP-SOTRE-ID}`


Parameters:

### Link IDs

store_id: The app store ID.
network: The network the event occurred on.
c: The campaign the event occured on.
cid: The campaign ID the event occured on.
ad: The ad the event occured on.
adid: The ad ID the event occured on.
ifa: The IFA (Identifier for Advertisers) of the user.
event_id: The event ID from the attribution platform.
event_time: The timestamp of the event in milliseconds since epoch.
link_uid: The unique identifier for the link.
oa_uid: The unique identifier for the user.

### In App IDs
event_uid: The unique identifier for the event. This is a randomly generated UUID to deduplicate events.
event_id: The event ID, such as "oa_app_open", "revenue" or "install" or "my_level_2_event".
event_time: The timestamp of the event in milliseconds since epoch.
revenue: The revenue of the event.

App Open Example:
```
https://demo.openattribution.dev/collect/events/123456789?ifa=00000000-0000-0000-0000-000000000000&event_time=1732003510046&event_uid=5730a99e-b009-41da-9d52-1315e26941c1&event_id=app_open&oa_uid=3bd9e091-fa6e-4b91-8dd1-503f8d4fe8f2
```


