import type { CalendarDate } from '@internationalized/date';

export interface NetworkEntry {
	id: number;
	network_name: string;
	network: string;
	status: string;
	is_custom: boolean;
}

export interface AppEntry {
	id: number;
	app_name: string;
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
	network_name: string;
	store_id: string;
	app_name: string;
	campaign_name: string;
	campaign_id: string;
	country_iso: string;
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

export interface GroupedPlotEntry {
	on_date: string;
	[key: string]: string | number;
	// value: number;
}

export interface DatesOverviewEntry extends OverviewEntry {
	on_date: string;
}

export type OverviewResponse = {
	overview: OverviewEntry[];
	dates_overview: DatesOverviewEntry[];
	networks: string[];
	store_ids: string[];
};

export type OverviewEntries = OverviewEntry[];

export type MyDateRange = {
	start: CalendarDate;
	end: CalendarDate;
};
