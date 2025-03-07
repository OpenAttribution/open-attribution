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

// To be used for generating retention percentages
export const retainedUserMetrics = [
	{ value: 'dx_1', label: 'D1 Retained Users' },
	{ value: 'dx_2', label: 'D2 Retained Users' },
	{ value: 'dx_3', label: 'D3 Retained Users' },
	{ value: 'dx_4', label: 'D4 Retained Users' },
	{ value: 'dx_5', label: 'D5 Retained Users' },
	{ value: 'dx_6', label: 'D6 Retained Users' },
	{ value: 'dx_7', label: 'D7 Retained Users' },
	{ value: 'dx_15', label: 'D15 Retained Users' },
	{ value: 'dx_30', label: 'D30 Retained Users' },
	{ value: 'dx_60', label: 'D60 Retained Users' },
	{ value: 'dx_90', label: 'D90 Retained Users' },
	{ value: 'dx_180', label: 'D180 Retained Users' },
	{ value: 'dx_365', label: 'D365 Retained Users' }
];

export const retainedUserMetricList = retainedUserMetrics.map(
	(metric) => metric.value
) satisfies readonly string[];

export const baseMetricsLabels = [
	{ value: 'impressions', label: 'Impressions' },
	{ value: 'clicks', label: 'Clicks' },
	{ value: 'installs', label: 'Installs' },
	{ value: 'revenue', label: 'Revenue' },
	{ value: 'dau', label: 'DAU' }
] as const;

export const specialMetricsLabels = [
	{ value: 'ctr', label: 'CTR' },
	{ value: 'ipm', label: 'IPM' }
] as const;

export const baseMetricsList = baseMetricsLabels.map(
	(metric) => metric.value
) satisfies readonly string[];

// Can be summed and divided freely, ie sum(impressions) / sum(clicks) = ctr
export const rawMetricsList = [...retainedUserMetricList, ...baseMetricsList] as const;

export const retentionLables = retainedUserMetricList.map((metric) => ({
	value: `ret_${metric}`,
	label: `${metric.toUpperCase().replace('DX_', 'D')} Retention`
}));

export const tableMetrics = [
	...baseMetricsLabels,
	...specialMetricsLabels,
	...retentionLables
] as const;
