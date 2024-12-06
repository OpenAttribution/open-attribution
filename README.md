# Open Attribution

An open source Mobile Measurement Platform (MMP) for tracking your mobile advertising spend and ROI.

## 🏗️🏗️🏗️ Under Construction 🏗️🏗️🏗️

If you're insterested in this project please feel free to reach out for collaboartion or more information.

[Chat on Discord](https://discord.gg/Z5ueYE3Ct3)

## Description

[OpenAttribution](https://openattribution.dev) is an open source mobile measurement platform (MMP) that tracks your mobile advertising spend from the ad impression and click then connects that to later in-app events. 

### This is done with several parts:

1. Impression, Click & Event Tracking on your domain
   1. `apps/postback-api`
2. Attribution of Mobile users and events to the impressions or clicks
   1. `apps/analytics-db`
      1. SQL in Clickhouse
      2. Ability for clients to set their own SQL for custom attribution logic
3. In-App Event Tracking  SDKs
   1. [OpenAttribution/oa-ios-sdk](https://github.com/OpenAttribution/oa-ios-sdk)
   2. [OpenAttribution/oa-android-sdk](https://github.com/OpenAttribution/oa-android-sdk)
4. Analytics Dashboard & Admin Panels
   1. `apps/dash-backend`
   2. `apps/dash-frontend`
   3. `apps/backend-db`

## True ownership of your mobile app's data

Own your advertising data without giving it over to a 3rd party processor. Our goal is to give developers their own ad tracking data. When users click on an app ad it's OK for the app to be tracking that data but user's don't want that data to be then passed on to other third parties.

Paying someone else to hold and manage your app's data takes power away from app creators. Open Attribution is a suite of open source tools so that you can manage your advertising data ownership.

## Open Source Community

Open Attribution is committed to building a community of developers who work together to build a secure ecosystem. The goal of having this as Open Source is to enable a community of advertisers who control the tracking of their adverstising campaigns and data.

## Interested in getting involved?

🏗️ This project is just starting, so if you're interested in using it please reach out before putting it into production. You can reach out on [Discord](https://discord.gg/Z5ueYE3Ct3) or email [hello@openattribution.dev](mailto:hello@openattribution.dev)

To read the work in progress documentation head to [Open Attribution Docs](https://openattribution.dev/docs/) to learn more.

### Why do apps NEED attribution?

If you want to buy in-app advertisements attribution a technical requirement, not a business option. Apps cannot use regular HTTP Urls to connect users, deep links are too limited. Historically MMPs stepped in to help solve this complex problem but by doing so became the arbiters of large amounts of data that some apps may wish to maintain control over. Read more about the [historical background here](https://openattribution.github.io/open-attribution/about/history).
