<script lang="ts">
	import Activity from 'lucide-svelte/icons/activity';
	import CreditCard from 'lucide-svelte/icons/credit-card';
	import DollarSign from 'lucide-svelte/icons/dollar-sign';
	import Users from 'lucide-svelte/icons/users';

	import { tableDimensions } from '$lib/constants';

	import * as Card from '$lib/components/ui/card/index.js';
	import * as Select from '$lib/components/ui/select/index.js';
	import DateRangePicker from '$lib/DateRangePicker.svelte';
	import type {
		MyDateRange,
		OverviewEntries,
		NetworkEntry,
		AppEntry,
		GroupedEntry,
		DatesOverviewEntry
	} from '../types';
	import { goto } from '$app/navigation';

	import StackedBar from '$lib/components/mycharts/StackedBar.svelte';

	import { page } from '$app/stores';

	import type { OverviewEntry } from '../types';

	import { type PageData } from './$types';
	import OverviewTable from '$lib/OverviewTable.svelte';
	import Multiselect from '$lib/Multiselect.svelte';

	const { data } = $props<{ data: PageData }>();

	let groupByDimA = $state('network_name');
	let groupByDimB = $state('app_name');
	let defaultDimA = { value: 'network', label: 'Network' };
	let defaultDimB = { value: 'store_id', label: 'App' };
	let totalImpressions = $state(0);
	let totalClicks = $state(0);
	let totalInstalls = $state(0);
	let totalRevenue = $state(0);

	function makeNewSum(newData: OverviewEntries) {
		if (newData && newData.length > 0) {
			// Generalize the summation for multiple fields
			const fieldsToSum = ['impressions', 'clicks', 'installs', 'revenue'] as const;

			// Reset the totals
			let totals: Record<(typeof fieldsToSum)[number], number> = {
				impressions: 0,
				clicks: 0,
				installs: 0,
				revenue: 0
			};

			// Loop over each entry and sum up the values for each field
			for (const entry of newData) {
				fieldsToSum.forEach((field) => {
					const value = entry[field];
					totals[field] += typeof value === 'number' ? value : 0;
				});
			}

			// Update the reactive states
			totalImpressions = totals.impressions;
			totalClicks = totals.clicks;
			totalInstalls = totals.installs;
			totalRevenue = totals.revenue;
		} else {
			console.log('makeSum not working!');
		}
	}

	function handleDateChange(newRange: MyDateRange | undefined) {
		if (newRange && newRange.start && newRange.end) {
			const startDate = newRange.start.toString();
			const endDate = newRange.end.toString();

			// Navigate to the same page with query parameters for start and end dates
			goto(`?start=${startDate}&end=${endDate}`);
		}
	}

	let filterNetworks = $state<string[]>([]);
	let filterApps = $state<string[]>([]);

	let filteredData = $state(getFilteredData(data.respData.overview));
	let filteredPlotData = $state(getFilteredPlotData(data.respData.dates_overview));
	let finalData = $state<GroupedEntry[]>([]);
	let finalPlotData = $state<GroupedEntry[]>([]);

	function getFilteredData(myData: OverviewEntry[]) {
		console.log('START FILTER');
		if (myData && myData.length > 0) {
			console.log('START FILTER2');
			filteredData = myData.filter((item) => {
				const networkMatch = filterNetworks.length === 0 || filterNetworks.includes(item.network);
				const appMatch = filterApps.length === 0 || filterApps.includes(item.store_id);
				return networkMatch && appMatch;
			});
		} else {
			console.log('START FILTER FAIL');
			return myData;
		}
		makeNewSum(filteredData);
	}

	function getFilteredPlotData(myData: DatesOverviewEntry[]) {
		console.log('START PLOT FILTER');
		if (myData && myData.length > 0) {
			console.log('START PLOT FILTER2');
			filteredPlotData = myData.filter((item) => {
				const networkMatch = filterNetworks.length === 0 || filterNetworks.includes(item.network);
				const appMatch = filterApps.length === 0 || filterApps.includes(item.store_id);
				return networkMatch && appMatch;
			});
		} else {
			console.log('START FILTER PLOT FAIL');
			return myData;
		}
	}

	function getFinalData(myData: OverviewEntry[]) {
		if (myData && myData.length > 0) {
			const returnedFinalData = groupByDimensions(myData, groupByDimA, groupByDimB);
			finalData = returnedFinalData;
		}
	}

	function getFinalPlotData(myData: DatesOverviewEntry[], groupByKey: string = 'network') {
		if (myData && myData.length > 0) {
			const returnedFinalPlotData = groupByDimensions(myData, 'on_date', groupByKey);
			finalPlotData = returnedFinalPlotData;
		}
	}

	function handleNetOptions(myRows: NetworkEntry[]) {
		let myOptions;

		myOptions = myRows.map((row) => ({
			value: row.network,
			label: row.network_name
		}));
		return myOptions;
	}

	function handleAppOptions(myRows: AppEntry[]) {
		let myOptions;

		// Fixing the second condition to check for apps
		myOptions = myRows.map((app) => ({
			value: app.store_id,
			label: app.app_name
		}));
		return myOptions;
	}

	function handleNetChange(event: CustomEvent<string[]>) {
		console.log('Selected net options:', event.detail);
		filterNetworks = event.detail;
		// Create a new URL object from the current location const url = new URL(window.location.href);
		// Get the existing query params
		const params = new URLSearchParams($page.url.search);

		// Set or update the 'networks' query parameter
		// TODO I think not currently being used to check for networks!
		params.set('networks', filterNetworks.join(','));

		// Navigate to the new URL, keeping other query parameters intact
		goto(`${$page.url.pathname}?${params.toString()}`);
	}

	function handleAppChange(event: CustomEvent<string[]>) {
		console.log('Selected app options:', event.detail);
		filterApps = event.detail;
	}

	function handleSelectGroupByChange(dimension: string, whichSelect: string) {
		if (whichSelect === 'A') {
			groupByDimA = dimension;
		} else if (whichSelect === 'B') {
			groupByDimB = dimension;
		}
	}

	interface GroupedData {
		[groupKey: string]: GroupedEntry;
	}

	function groupByDimensions(
		filteredData: OverviewEntry[],
		dimensionA: string,
		dimensionB: string
	) {
		console.log('GROUPING');

		const groupedData = filteredData.reduce<GroupedData>((acc, curr) => {
			const keyA = curr[dimensionA] as string;
			const keyB = curr[dimensionB] as string;
			const groupKey = `${keyA}|${keyB}`;

			if (!acc[groupKey]) {
				acc[groupKey] = {
					[dimensionA]: keyA,
					[dimensionB]: keyB,
					impressions: 0,
					clicks: 0,
					installs: 0,
					revenue: 0
				};
			}

			acc[groupKey].impressions += curr.impressions || 0;
			acc[groupKey].clicks += curr.clicks || 0;
			acc[groupKey].installs += curr.installs || 0;
			acc[groupKey].revenue += curr.revenue || 0;

			return acc;
		}, {});

		const myfinalData = Object.values(groupedData);
		return myfinalData;
		console.log('FINAL DATA ROWS:', finalData.length);
	}

	function formatNumber(num: number) {
		return num.toLocaleString();
	}
</script>

<div class="flex min-h-screen w-full flex-col">
	<main class="flex flex-1 flex-col gap-4 p-4 md:gap-8 md:p-8">
		<div class="grid gap-20 md:grid-cols-3">
			<Card.Root>
				<Card.Header class="flex flex-row items-center justify-between space-y-0 pb-2">
					<Card.Title class="text-sm font-large">Apps</Card.Title>
				</Card.Header>
				<Card.Content>
					{#await data.respData}
						Loading...
					{:then mydata}
						{#if mydata.store_ids && mydata.store_ids.length > 0}
							<Multiselect
								options={handleAppOptions(mydata.store_ids)}
								placeholder="Filter by App"
								on:change={handleAppChange}
							/>
						{:else}
							No apps yet.
						{/if}
					{/await}
				</Card.Content>
			</Card.Root>
			<Card.Root>
				<Card.Header class="flex flex-row items-center justify-between space-y-0 pb-2">
					<Card.Title class="text-sm font-large">Networks</Card.Title>
				</Card.Header>
				<Card.Content>
					{#await data.respData}
						Loading...
					{:then myData}
						{#if myData.networks && myData.networks.length > 0}
							<Multiselect
								options={handleNetOptions(myData.networks)}
								placeholder="Filter by Network"
								on:change={handleNetChange}
							/>
						{:else}
							No networks.
						{/if}
					{/await}
				</Card.Content>
			</Card.Root>
			<Card.Root>
				<Card.Header class="flex flex-row items-center justify-between space-y-0 pb-2">
					<Card.Title class="text-sm font-large">Dates</Card.Title>
				</Card.Header>
				<Card.Content>
					<DateRangePicker onChange={handleDateChange} />
				</Card.Content>
			</Card.Root>
		</div>

		<div class="grid gap-4 md:grid-cols-2 md:gap-8 lg:grid-cols-4">
			<Card.Root>
				<Card.Header class="flex flex-row items-center justify-between space-y-0 pb-2">
					<Card.Title class="text-sm font-medium">Impressions</Card.Title>
					<Users class="text-muted-foreground h-4 w-4" />
				</Card.Header>
				{#await data.respData}
					Loading...
				{:then mydatas}
					<Card.Content>
						<div class="text-2xl font-bold">{formatNumber(totalImpressions)}</div>
						<p class="text-muted-foreground text-xs">+19% from last month?</p>
					</Card.Content>
				{/await}
			</Card.Root>
			<Card.Root>
				<Card.Header class="flex flex-row items-center justify-between space-y-0 pb-2">
					<Card.Title class="text-sm font-medium">Clicks</Card.Title>
					<CreditCard class="text-muted-foreground h-4 w-4" />
				</Card.Header>
				{#await data.respData}
					Loading...
				{:then mydatas}
					<Card.Content>
						<div class="text-2xl font-bold">{formatNumber(totalClicks)}</div>
						<p class="text-muted-foreground text-xs">
							{#if totalImpressions > 0}
								{((totalClicks / totalImpressions) * 100).toFixed(2)}%
							{:else}
								--
							{/if}
							Click Through Rate
						</p>
					</Card.Content>
				{/await}
			</Card.Root>
			<Card.Root>
				<Card.Header class="flex flex-row items-center justify-between space-y-0 pb-2">
					Installs
					<Activity class="text-muted-foreground h-4 w-4" />
				</Card.Header>
				{#await data.respData}
					Loading...
				{:then mydatas}
					<Card.Content>
						<div class="text-2xl font-bold">
							{formatNumber(totalInstalls)}
						</div>
						<p class="text-muted-foreground text-xs">
							{#if totalImpressions > 0}
								{(totalInstalls / (totalImpressions / 1000)).toFixed(2)}
								Installs Per Mille
							{:else}
								--
							{/if}
						</p>
					</Card.Content>
				{/await}
			</Card.Root>
			<Card.Root>
				<Card.Header class="flex flex-row items-center justify-between space-y-0 pb-2">
					<Card.Title class="text-sm font-medium">Total Revenue</Card.Title>
					<DollarSign class="text-muted-foreground h-4 w-4" />
				</Card.Header>
				{#await data.respData}
					Loading...
				{:then mydatas}
					<Card.Content>
						<div class="text-2xl font-bold">
							{totalRevenue.toLocaleString('en-US', {
								style: 'currency',
								currency: 'USD'
							})}
						</div>
						<p class="text-muted-foreground text-xs">+19% from last month</p>
					</Card.Content>
				{/await}
			</Card.Root>
		</div>

		<div class="h-[300px] p-4 border rounded">
			{#await data.respData}
				Loading...
			{:then mydata}
				{#if mydata.dates_overview && mydata.dates_overview.length > 0}
					{getFilteredPlotData(mydata.dates_overview)}
					{getFinalPlotData(filteredPlotData || [], (groupByKey = 'network'))}
					<StackedBar plotData={finalPlotData}></StackedBar>
					<!-- <OverviewTable
								overviewData={finalDatao}
								dimensionA={groupByDimA}
								dimensionB={groupByDimB}
							></OverviewTable> -->
				{:else}
					Loading...
				{/if}
			{/await}
		</div>

		<div class="gap-4 md:gap-8">
			<Card.Root class="xl:col-span-2">
				<Card.Header class="flex flex-row items-center">
					<div class="gap-2">
						<Card.Title>Overview</Card.Title>
						<Card.Description>Recent data.</Card.Description>
						<div class="flex p-2 gap-4">
							<Select.Root portal={null} selected={defaultDimA}>
								<Select.Trigger class="w-[180px]">
									<Select.Value placeholder="Select Group By DimensionB" />
								</Select.Trigger>
								<Select.Content>
									<Select.Group>
										<Select.Label>Fruits</Select.Label>
										{#each tableDimensions as dimension}
											<Select.Item
												value={dimension.value}
												label={dimension.label}
												on:click={() => handleSelectGroupByChange(dimension.value, 'A')}
												>{dimension.label}</Select.Item
											>
										{/each}
									</Select.Group>
								</Select.Content>
								<Select.Input name="favoriteFruitA" />
							</Select.Root>

							<Select.Root portal={null} selected={defaultDimB}>
								<Select.Trigger class="w-[180px]">
									<Select.Value placeholder="Select Group By DimensionB" />
								</Select.Trigger>
								<Select.Content>
									<Select.Group>
										<Select.Label>Ad Networks</Select.Label>
										{#each tableDimensions as dimension}
											<Select.Item
												value={dimension.value}
												label={dimension.label}
												on:click={() => handleSelectGroupByChange(dimension.value, 'B')}
												>{dimension.label}</Select.Item
											>
										{/each}
									</Select.Group>
								</Select.Content>
								<Select.Input name="favoriteFruitB" />
							</Select.Root>
						</div>
					</div>
				</Card.Header>
				<Card.Content>
					{#await data.respData}
						Loading...
					{:then mydata}
						{#if mydata.overview && mydata.overview.length > 0}
							{getFilteredData(mydata.overview)}
							{getFinalData(filteredData || [])}
							{console.log('FINAL DATA GBA: ', groupByDimA)}
							<OverviewTable
								overviewData={finalData}
								dimensionA={groupByDimA}
								dimensionB={groupByDimB}
							></OverviewTable>
						{:else}
							Loading...
						{/if}
					{/await}
				</Card.Content>
			</Card.Root>
		</div>
	</main>
</div>
