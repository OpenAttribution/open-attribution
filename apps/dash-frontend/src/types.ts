import type { CalendarDate } from '@internationalized/date';

export interface NetworkEntry {
	id: number;
	name: string;
	postback_id: string;
	status: string;
	is_custom: boolean;
}

export interface AppEntry {
	id: number;
	name: string;
	store_id: string;
	status: string;
}

export type NetworkEntries = {
	networks: NetworkEntry[];
};

export type NetworkResponse = {
	respData: NetworkEntries;
};

export interface OverviewEntry {
	[key: string]: string | number;
	network: string;
	store_id: string;
	campaign_name: string;
	campaign_id: string;
	impressions: number;
	clicks: number;
	installs: number;
	revenue: number;
}

export interface GroupedEntry {
	[key: string]: string | number;
	impressions: number;
	clicks: number;
	installs: number;
	revenue: number;
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
	revenue: number;
}

export type OverviewResponse = { overview: OverviewEntry[]; dates_overview: DatesOverviewEntry[] };

export type OverviewEntries = OverviewEntry[];

export type MyDateRange = {
	start: CalendarDate;
	end: CalendarDate;
};
