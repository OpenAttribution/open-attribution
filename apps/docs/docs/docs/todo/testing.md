# Testing

## Postback API End to End Testing
The testing is run in `postback-api/tests` which will be run by the development docker as `postback-test`.

### Specific Tests
These are run by `postback-api/tests/test_installs.py` which runs through a series of events and checks the results in the database.  These are for example:

- Click -> App Open: This is should be an install.
- Click -> Click: This should not be an install.
- App Open -> App Open: This is an organic install, not attributable.
- App Open -> Click: This is an organic install, not attributable.
etc

This has currently shown that when firing dozens of events at once, some mismatches in the OLAP database are inevitable. This might be a cause to look into a more robust event queue system or some other approach. The pros of the OLAP for quickly aggregating live data are still good though.


### Continuous Random Testing

The `postback-api/tests/generate_impressions_and_clicks.py` script is designed to randomly generate events for testing. This is currently configured to run indefinitely. Data is so random as to be rather flat. But good for working on the frontend dash.

