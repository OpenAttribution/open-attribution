
!!! TODO 
	This section is currently a design plan
	

The database needs two sections:

1. Admin: Daily operations of the MMP which will require
	1. Company
		1. Apps
			1. App Events
		2. Users
			1. Permissions per app
			2. General admin permissions
		3. Network Connections
			1. Data access control
			2. Pull spend API keys
2. Combined & Aggregated Analytics: highest level tables for returning data to client dashboards
	1. Dimensions
		1. Apps
		2. Networks
		3. Campaigns
		4. Adgroups
		5. Ads
		6. Assets
	2. Aggregated data tables, with attribution data
		1. clicks, impressions -> from click links
		2. installs, retention -> from app open events
		3. event counts -> from app events
		4. revenue, roas -> from app revenue events
		5. spend -> from network reports
	3. Attribution model data
		1. table of users and their attribution data

