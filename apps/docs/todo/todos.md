This project was started around Nov 10th, 2023 and is still very pre-alpha stage. Thus this page will serve to help put some context for how much work is still needed for an MVP product.

## Testing
Make plan for testing regimen. To test:
1. Per user: 
	1. 1 impression, 1 click, 1 install
	2. 1 impression, 1 install
	3. 1 impression, 1 click, 1 install, 1 click (shouldn't be counted)
	4. 1 impression, 1 install, 1 click (shouldn't be counted) 
	5. 2 impression, 1 install
	6. 2 clicks, 1 install
	7. 2 impressions, 2 clicks, 1 install
		1. 

## Documentation
Some parts of documentation will need to be even more detailed and specific. They will be dealing with the ops side, so perhaps they should even be moved to somewhere unique or different?

#### SDK Setup
Documentation for the iOS and Android developers. It would also presumably fit well with Unity and Unreal as well.

#### Tracking links
Tracking link setups for marketers.

#### Marketing & Campaign Management
This is definitely high level, but a good knowledgebase for users would be good. Other MMPs have great resources, and a community managed one would be good as well.

## Data Pipeline
The date pipeline is the infrastructure underlying this entire project. The balancing act here has proved challenging in trying to design something that can be scaled down enough to provide a low cost option for lower volume amounts. Building a pipeline that can scale to handle large volume of data is at odds with a single instance that can be launched on one server. Any help here would be appreciated.
- [ ] Decide plan that can work for $100 a month est cloud spend but still be scaled up for a large client
- [ ] Build new launcher.sh for data pipeline

## Database
The database for now will depend heavily on the data flow for the pipeline, so for now these todos are very high level.
- [ ] Admin & Users
- [ ] Companies, Apps
- [ ] Network Data connections


### MMP Analytics Dashboard
These will be the applications for the JS site wrapping the analytics dashboard.
- [ ] Login & User Authentication
- [ ] User Management
- [ ] Companies Page
- [ ] Dash page
	- [ ] Apps
	- [ ] Campaigns
- [ ] Data connections page (in/out)

### Business site
- [ ] Build Svelte App
- [ ] Pages
	- [x] Home & Marketing
	- [ ] Road map
	- [ ] How to contribute
	- [x] About
