
We will need a new service, preferrably Python, for pulling impression, click and spend reports from the ad networks. There is an open question of where to store this data. This will ultimately be joined with the postback data before landing on the dash.

- [ ] Where to store?
	- [ ] ClickHouse vs PostgreSQL
- [ ] Python service to regularly crawl/pull batch data from each defined network.
- [ ] Processing pipeline for this data. Perhaps storing raw data on S3?
- [ ] Where to combine?

