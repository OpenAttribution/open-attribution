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
	user_sessions: number;
	dau: number;
	dx_1: number;
	dx_2: number;
	dx_3: number;
	dx_4: number;
	dx_5: number;
	dx_6: number;
	dx_7: number;
	dx_15: number;
	dx_30: number;
	dx_60: number;
	dx_90: number;
	dx_180: number;
	dx_365: number;
}

export interface GroupedEntry {
	[key: string]: number | string;
	impressions: number;
	clicks: number;
	installs: number;
	revenue: number;
	user_sessions: number;
	dau: number;
	dx_1: number;
	dx_2: number;
	dx_3: number;
	dx_4: number;
	dx_5: number;
	dx_6: number;
	dx_7: number;
	dx_15: number;
	dx_30: number;
	dx_60: number;
	dx_90: number;
	dx_180: number;
	dx_365: number;
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
