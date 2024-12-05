# Analytics Services Architecture

The `analytics-db` service is responsible for storing and processing event data. It is currently a ClickHouse database with various materialized views and aggregations that handle the impression, click and attributions.

## Core requirements

Other than a simple daily count of impressions, clicks andinstalls, the following are all still TODO:

- Attributed installs and events should be stored in the database.
- DAU: daily active users (not a great metric, but useful for getting started working on the retention)
- Retention metrics: d1 - d7, d15, d30, d60, d90
- Retention events: dx of events (eg d1_tutorial_complete)
- Revenue metrics

## Further Notes

### Core Event Handling
- Event types: impressions, clicks, purchases, etc.
  - Strategy: Keep data processing on device when possible
  - Allow apps to maintain their own event ontology
  - Data science/ML teams handle normalization

### Attribution Flow
- Route attributable events to attribution service
  - Define time windows for fresh installs vs reengagement
  - Optimize attribution service costs
  - Consider high-volume event platform for non-attribution events

### AdAttributionKit Management
- Client configuration capabilities:
  - Customizable conversion values
  - Flexible event type mapping
  - Bit array data mapping for Apple's framework

### Link Attribution
- Implement ephemeral link click tracking
  - Store minimal data: user agent, IP address, timestamp
  - Focus on install attribution within time window
  - Consider value of tracking app opens vs installs only

## Experiments Service

### Device-First Architecture
- Leverage on-device user history
- Implementation approach:
  - Simple behavioral rules
  - Device-side ML model execution
  - Anonymous data summaries
  - Minimize identifier usage

## Attribution Service

### Integration Options
- SAN (Self-Attributing Networks) support
  - MMP status requirements
  - Audit compliance
- AdAttributionKit integration for postbacks
- Data export capabilities
  - Client system integration
  - Potential open-source solution
- Server-to-Server (S2S) integration
  - Support for SDK-less attribution
  - Consider open-source offering for self-hosting
