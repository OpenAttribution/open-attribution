export const tableDimensions = [
	{ value: 'network_name', label: 'Ad Network' },
	{ value: 'app_name', label: 'App' },
	{ value: 'campaign_name', label: 'Campaign Name' },
	{ value: 'campaign_id', label: 'Campaign ID' },
	{ value: 'country_iso', label: 'Country Code' },
	{ value: 'ad_name', label: 'Ad Name' },
	{ value: 'ad_id', label: 'Ad ID' }
];

// const tableMetrics = [
//     { value: 'impressions', label: 'Impressions' },
//     { value: 'clicks', label: 'Clicks' },
//     { value: 'installs', label: 'Installs' },
//     { value: 'revenue', label: 'Revenue' }
// ];

export const metrics = [
	'impressions',
	'clicks',
	'installs',
	'revenue',
	'dx_1',
	'dx_2',
		'dx_3',
		'dx_4',
		'dx_5',
		'dx_6',
		'dx_7',
		'dx_15',
		'dx_30',
		'dx_60',
		'dx_90',
		'dx_180',
		'dx_365'
	] as const;