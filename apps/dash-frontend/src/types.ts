export interface OverviewEntry {
	on_date: string;
	network: string;
	store_id: string;
	campaign_name: string;
	campaign_id: string;
	ad_name: string;
	ad_id: string;
	impressions: number;
	clicks: number;
	installs: number;
	revenue: string;
}

export type OverviewEntries = OverviewEntry[];
