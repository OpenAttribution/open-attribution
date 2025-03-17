---
draft: false

date: 2025-03-17

authors:
  - ddxv

categories:
  - Updates
---

# DAU and GDC

The frontend dash has come along enough that it's starting to be slightly useful as a basic DAU/Install dashboard. It's certainly still basic, and I'm unsure how much of it will stick around in the future, but as a way of verifying the underlying data it is coming along well.

Now the dash has DAU, Install, and Retention metrics, it starts to be time to add some of the more complex metrics like spend, revenue, and events.

## Importing Impressions and Spend from Ad Networks

This is going to be a long ranging task, but an initial import and mixing of the streaming postback data and the aggregated ad network data will be an essential step for the upcoming MVP.

Finding an ad network and an app/game to test with is the next step. I will probably start with some small testing of my own app with some basic ad spend on Facebook or TikTok. Once a basic setup is there, I will need to finalize the frontend authentication and reach out to the community to see if any developers are willing to share their data for testing in an alpha MVP.

## Events

This one I've been holding off on as I'm less sure of the usecases. In my experience there are a lot of different usecases and it might be best to wait until I have a requirement to add them.

## Revenue

This one requires the handling of currencies and some logic for converting them to a single currency. This one I should be able to do at some point in the future, but it's not a priority yet.

## GDC 2025

I just got into San Francisco and will be around GDC for the coming days. If you'd like to discuss Open Attribution further, please reach out!
