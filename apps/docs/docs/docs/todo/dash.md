# Dashboard Components

The dash is comprised of `dash-backend` and `dash-frontend` (svelte).

## Features Needed

### Authentication
- [ ] **Auth Login**: While required for any real use, as the main way of sharing this project is the demo, I think this can wait for now. Possibly use Lucia Auth for a fully featured authentication setup. 
  - **Note**: Marketing is often contracted out, and marketing teams often handle more than one client. Need clear separation of roles. At least owners, apps, and contractors.
- [ ] **Network Authentication**: CRUD tools for saving various network authentication secrets in the `admin-db`. This is currently broken/not working.

### Data Management
- [ ] **Drill Down**: The dash needs to start building out a drilldown feature for digging into deeply nested data. An alternative might be a more flexible group-by table like those in various BI tools.

### Integration
- Consider allowing integration with 3rd party dashboards.

## Links Management

### Link Generation
- Functional payload, ads metadata

### Link Shortening
- For platforms with strict text limits, which is most social platforms.

### Dynamic Link Payload
- Can change redirect behavior and payload post-facto
- TTL - recommended to limit server cost, ads links go dead after a while

### Static Link Payload
- Cheap enough to not expire

### Issues to Handle
- **Link Abuse**: Link shorteners are often used in phishing attacks. Caution against overuse here. This is a constant battle!
- **Link Rot**: Promos end, sites get refactored, apps get refactored. Degrade gracefully, at least land on a home page or current promos page.
- **Ad Blockers**: Do NOT break functionality for ads data! The whole point is for a user to install, engage, etc. Link payload lookup API should be purely functional!