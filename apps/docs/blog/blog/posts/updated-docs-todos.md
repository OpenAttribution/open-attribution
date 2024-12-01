---
draft: false


date: 2024-10-18

authors: 
  - ddxv

categories:
  - Updates
---

# Updated Docs and Todos

Trying to get the docs and todos in order I cleaned up the docker sections, removed mentions of the older local dev setup.

To show how much there is left to do I added several sections to the todos, which should largely cover the checklists for finishing an MVP. That's these items from last time:


## Still More to Do

- [ ] Tons more work to finish MVP of frontend: authentication, reporting levels, creatives, spend, revenue, revents
- [ ] Rewrite Docker documentation
- [ ] Remove old non-Docker documentation
- [ ] Create testing section for frontend
- [ ] Pull data from first ad network
- [ ] Start iOS and/or Android SDK

Additionally I did some more house cleaning by moving the prettier and eslint configs to the root of the repo. Hopefully this simplifies things for new comers to the code, though I'm still having some issues with the prettier-svelte-plugin, but that might just be due to missing Svelte 5 support.
