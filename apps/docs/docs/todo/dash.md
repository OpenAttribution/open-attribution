The dash is comprised of `dash-backend` and `dash-frontend` (svelte).

The dash is currently lacking these features


- [ ] Auth Login: While required for any real use, as the main way of sharing this project is the demo, I think this can wait for now. Possibly use Lucia Auth as an easy way of getting a fully featured authentication setup.
- [ ] Dash Plots: Currently the frontend does not have any plotting. These features are set to change hundreds of times, so the plotting library is not crucial now, but we do need something setup to help show how OpenAttribution can be used and for testing data. I think using shadcn-svelte's upcoming charts might be a good option for this as they are very basic, but have a unified style.
- [ ] Drill down: The dash needs to start building out a drilldown feature for digging into deeply nested data. An alternative to drill down might be a more flexible group-by table like you find in various BI tools.
- [ ] Network Authentication: CRUD tools for saving various network authentication secrets in the `admin-db`
- [ ] Tracking links: Tracking link setups for marketers.
