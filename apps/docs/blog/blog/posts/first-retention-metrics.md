---
draft: false

date: 2025-02-07

authors:
  - ddxv

categories:
  - Updates
---
``
# First Retention Metrics & Plans for GDC 2025

I started working on an MVP for retention metrics since the `app_open` was the first event added to the Android SDK. I decided to do the retention calculations in ClickHouse materialized views which keeps with the current flow.

ClickHouse I continue to be unsure about it's future. It's very large for the testing and small indie developer usecases, but it's quick turnaround from data to frontend is very nice. Additionally, the `REFRESHABLE VIEWS` are easy to use and understand. I keep struggling when I use regular Aggregation Tables, as they have different results depending on when/how the data gets inserted, hence the heavy use of `REFRESHABLE VIEWS`.

To compliment this I added Retention values to the frontend dash as well, though my pretty low frontend skills there are holding back the dash quite a bit. But I did expand the plotting a bit, as it of course helps with troubleshooting / adding features for the backend.

## Plans for GDC 2025

I'm excited to be going to GDC 2025 in San Francisco. I'll be doing it on a budget, but hopefully getting started early I can make some noise and meet some good people. I'd like to find a way to connect with other people interested in the open source scene, which is oddly a bit of a challenge for this 'developer' conference when most of it is focused on the larger corporate companies.

If you'd like to meet up, please reach out!
