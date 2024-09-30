import type { CalendarDate } from '@internationalized/date';

export interface NetworkEntry {
	name: string;
}



export type NetworkEntries = NetworkEntry[];

export interface OverviewEntry {
	network: string;
	store_id: string;
	campaign_name: string;
	campaign_id: string;
	impressions: number;
	clicks: number;
	installs: number;
	revenue: string;
}

export interface DatesOverviewEntry {
	on_date: string;
	network: string;
	store_id: string;
	campaign_name: string;
	campaign_id: string;
	impressions: number;
	clicks: number;
	installs: number;
	revenue: string;
}

export type OverviewResponse = { overview: OverviewEntry[]; dates_overview: DatesOverviewEntry[] };

export type OverviewEntries = OverviewEntry[];

export type MyDateRange = {
	start: CalendarDate;
	end: CalendarDate;
};
