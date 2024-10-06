---
draft: false


date: 2024-10-06

authors: 
  - ddxv

categories:
  - Updates
---

# Analytics Dash: Switch from Superset to Custom Svelte

After quite a long break I got back into working on Open Attribution. My point of re-entering was to finally start working on the `admin-db` which would house all the user facing settings and analytics dashboard. 

This very quickly brought up the issue of Superset, a no code drop in fully customizeable analytics dashboard. I was loving it, but trying to get it to work for my usecase always ended up being a time suck, and as I moved towards a more managed approach Superset wouldn't be a good fit. Maybe we can go back to it in the future.

So with that, we changed the frontend dash quite a bit. The analytics dashboard now consists of 3 apps:

  1. `admin-db`: a postgres database for managing the tables for things like users, authentication, netowrks, apps etc. 
  2. `dash-backend`: a python Litestar backend API, currently only exposed to localhost
  3. `dash-frontend`: a svelte frontend for managing the analytics dashboard. We also switched from `skeleton` to `shadcn` due to wanting to start building this project with Svelte 5 to be well positioned for the future (and because I wanted to try it out).

## Docker Re-Do

Meanwhile, I've also completely revamped the docker environment for development / deployment. A big part of this was due to removing Superset, which had come with a lof of it's own docker baggage, and more just because I'm still learning Docker.


## More to Do

- [ ] Tons more work to finish MVP of frontend: authentication, reporting levels, creatives, spend, revenue, revents
- [ ] Rewrite Docker documentation
- [ ] Remove old non-Docker documentation
- [ ] Create testing section for frontend
- [ ] Pull data from first ad network
- [ ] Start iOS and/or Android SDK

Some features are live at [demo.openattribution.com](http://demo.openattribution.com).
