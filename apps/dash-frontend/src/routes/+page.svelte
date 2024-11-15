<script lang="ts">
	import Activity from 'lucide-svelte/icons/activity';
	import CreditCard from 'lucide-svelte/icons/credit-card';
	import DollarSign from 'lucide-svelte/icons/dollar-sign';
	import Users from 'lucide-svelte/icons/users';
	import { onMount } from 'svelte';

	// Can't get this working due to renderComponent not working, not sure if this is the right way to do it
	// https://github.com/huntabyte/shadcn-svelte/blob/next/sites/docs/src/routes/(app)/examples/tasks/(components)/columns.ts
	// import DataTableColumnHeader from '$lib/my-table/column-header.svelte';

	import { tableDimensions } from '$lib/constants';

	import MyOverviewTable from '$lib/my-table/MyOverviewTable.svelte';

	import * as Card from '$lib/components/ui/card/index.js';
	import * as Select from '$lib/components/ui/select/index.js';
	import DateRangePicker from '$lib/DateRangePicker.svelte';
	import type {
		MyDateRange,
		NetworkEntry,
		AppEntry,
		GroupedEntry,
		GroupedPlotEntry,
		DatesOverviewEntry
	} from '../types';
	import { goto, invalidateAll, invalidate } from '$app/navigation';

	import StackedBar from '$lib/components/mycharts/StackedBarChart.svelte';

	import { page } from '$app/stores';

	import type { OverviewEntry } from '../types';

	import { type PageData } from './$types';
	import OverviewTable from '$lib/OverviewTable.svelte';
	import Multiselect from '$lib/Multiselect.svelte';

	const pageDefaultDimA = 'network_name';
	const pageDefaultDimB = 'campaign_name';

	let groupByDimA = $state(pageDefaultDimA);
	let groupByDimB = $state(pageDefaultDimB);

	interface Props {
		data: PageData;
	}

	let filterNetworks = $state<string[]>([]);
	let filterApps = $state<string[]>([]);

	let { data }: Props = $props();
	let stateData = $state(data.respData.overview);
	let statePlotData = $state(data.respData.dates_overview);
	let filteredData = $derived(getFilteredData(stateData, filterNetworks, filterApps));

	let totalImpressions = $derived(makeNewSum(filteredData, 'impressions'));
	let totalClicks = $derived(makeNewSum(filteredData, 'clicks'));
	let totalInstalls = $derived(makeNewSum(filteredData, 'installs'));
	let totalRevenue = $derived(makeNewSum(filteredData, 'revenue'));

	let finalData = $derived(
		getFinalData(getFilteredData(stateData, filterNetworks, filterApps), groupByDimA, groupByDimB)
	);

	let finalPlotData = $derived(
		getFinalPlotData(getFilteredPlotData(statePlotData, filterNetworks, filterApps), groupByDimA)
	);

	function getColumns(myGroupByDimA: string, myGroupByDimB: string) {
		const columnATitle =
			tableDimensions.find((dim) => dim.value === myGroupByDimA)?.label || myGroupByDimA;
		const columnBTitle =
			tableDimensions.find((dim) => dim.value === myGroupByDimB)?.label || myGroupByDimB;

		// Create columns for the selected dimensions first
		const selectedDimensionColumns = [
			{
				accessorKey: myGroupByDimA,
				header: columnATitle
			},
			{
				accessorKey: myGroupByDimB,
				header: columnBTitle
			}
		];

		// // Create columns for all remaining dimensions
		// const remainingDimensionColumns = tableDimensions
		// 	.filter((dim) => dim.value !== myGroupByDimA && dim.value !== myGroupByDimB)
		// 	.map((dim) => ({
		// 		accessorKey: dim.value,
		// 		header: dim.label
		// 	}));

		// Add the metric columns
		const metricColumns = [
			{
				accessorKey: 'impressions',
				header: 'Impressions'
			},
			{
				accessorKey: 'clicks',
				header: 'Clicks'
			},
			{
				accessorKey: 'installs',
				header: 'Installs'
			},
			{
				accessorKey: 'revenue',
				header: 'Revenue'
			}
		];

		// const myCols = [...selectedDimensionColumns, ...remainingDimensionColumns, ...metricColumns];
		const myCols = [...selectedDimensionColumns, ...metricColumns];
		console.log('Data table columns:', myCols.map((col) => col.accessorKey).join(', '));
		return myCols;
	}

	let columns = $derived(getColumns(groupByDimA, groupByDimB));

	function makeNewSum(newData: OverviewEntry[], metric: string) {
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
			if (metric === 'impressions') {
				return totals.impressions;
			} else if (metric === 'clicks') {
				return totals.clicks;
			} else if (metric === 'installs') {
				return totals.installs;
			} else if (metric === 'revenue') {
				return totals.revenue;
			}
		} else {
			console.log('makeSum not working! metric=', metric);
			return 0;
		}
		return -1;
	}

	function handleDateChange(newRange: MyDateRange | undefined) {
		if (newRange && newRange.start && newRange.end) {
			const startDate = newRange.start.toString();
			const endDate = newRange.end.toString();

			console.log('handleDateChange', startDate, endDate);

			invalidate('app:dates');

			// Navigate to the same page with query parameters for start and end dates
			goto(`?start=${startDate}&end=${endDate}`, {
				invalidateAll: true,
				replaceState: true
			});

			invalidateAll();
		}
	}

	function getFilteredData(
		myData: OverviewEntry[],
		myFilterNetworks: string[],
		myFilterApps: string[]
	) {
		// console.log('DATA FILTER START:', myData.length);
		let myFilteredData: OverviewEntry[] = [];
		if (myData && myData.length > 0) {
			// console.log('DATA FILTER LOOP:', myData.length);
			myFilteredData = myData.filter((item) => {
				const networkMatch =
					myFilterNetworks.length === 0 || myFilterNetworks.includes(item.network);
				const appMatch = myFilterApps.length === 0 || myFilterApps.includes(item.store_id);
				return networkMatch && appMatch;
			});
		} else {
			// console.log('DATA FILTER FAIL');
			myFilteredData = myData;
		}
		// console.log('DATA FILTER END:', myFilteredData.length);
		return myFilteredData;
	}

	function getFilteredPlotData(
		myData: DatesOverviewEntry[],
		myFilterNetworks: string[],
		myFilterApps: string[]
	) {
		let myFilteredData: DatesOverviewEntry[] = [];
		console.log('PLOT FILTER START myData=', myData.length);
		if (myData && myData.length > 0) {
			myFilteredData = myData.filter((item) => {
				const networkMatch =
					myFilterNetworks.length === 0 || myFilterNetworks.includes(item.network);
				const appMatch = myFilterApps.length === 0 || myFilterApps.includes(item.store_id);
				return networkMatch && appMatch;
			});
		} else {
			// console.log('PLOT FILTER FAIL myData=', myData);
			myFilteredData = myData;
		}
		console.log('PLOT FILTER END myFilteredData=', myFilteredData.length);
		return myFilteredData;
	}

	function getFinalData(myData: OverviewEntry[], myGroupByDimA: string, myGroupByDimB: string) {
		// console.log('DATA FINAL START:', myData.length);
		let myReturnedFinalData: GroupedEntry[] = [];
		if (myData && myData.length > 0) {
			// console.log('DATA FINAL LOOP:', myData.length);
			myReturnedFinalData = groupByDimensions(myData, myGroupByDimA, myGroupByDimB);
			// console.log('DATA FINAL LOOP END:', myReturnedFinalData.length);
		} else {
			// console.log('DATA finalData was given empty list');
			myReturnedFinalData = myData;
		}
		// console.log('DATA FINAL END:', myReturnedFinalData.length);
		return myReturnedFinalData;
	}

	function getFinalPlotData(myData: DatesOverviewEntry[], groupByKey: string = 'network') {
		let myReturnedFinalPlotData: GroupedPlotEntry[] = [];
		if (myData && myData.length > 0) {
			myReturnedFinalPlotData = groupByDimensionsPlot(myData, groupByKey, 'installs');
		} else {
			console.log('PLOT finalPlotData was given empty list');
			myReturnedFinalPlotData = [];
		}
		return myReturnedFinalPlotData;
	}

	function handleNetOptions(myRows: NetworkEntry[]) {
		let myOptions;

		myOptions = myRows
			.filter((row) => row.network) // Ensures only rows with a network are processed
			.map((row) => ({
				value: row.network,
				label: row.network_name || row.network
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
		console.log('SELECT net options:', event.detail);
		filterNetworks = event.detail;
		// Create a new URL object from the current location const url = new URL(window.location.href);
		// Get the existing query params
		const params = new URLSearchParams($page.url.search);

		// Set or update the 'networks' query parameter
		// TODO I think not currently being used to check for networks!
		params.set('networks', filterNetworks.join(','));

		// Navigate to the new URL, keeping other query parameters intact
		goto(`${$page.url.pathname}?${params.toString()}`, {
			invalidateAll: true,
			replaceState: true
		});
	}

	function handleAppChange(event: CustomEvent<string[]>) {
		console.log('SELECT app options:', event.detail);
		filterApps = event.detail;
	}

	let titleGroupByA = $derived(handleGroupByChange(groupByDimA));
	let titleGroupByB = $derived(handleGroupByChange(groupByDimB));

	function handleGroupByChange(dimension: string) {
		let myTitle = tableDimensions.find((dim) => dim.value === dimension)?.label || dimension;
		return myTitle;
	}

	// function handleSelectGroupByChange(dimension: string, whichSelect: string) {
	// 	if (whichSelect === 'A') {
	// 		groupByDimA = dimension;
	// 	} else if (whichSelect === 'B') {
	// 		groupByDimB = dimension;
	// 	}
	// }

	interface GroupedData {
		[groupKey: string]: GroupedEntry;
	}

	interface GroupedPlotData {
		[groupKey: string]: GroupedPlotEntry;
	}

	function groupByDimensions(
		myFilteredData: OverviewEntry[],
		dimensionA: string,
		dimensionB: string
	) {
		// console.log('GROUPING', dimensionA, dimensionB);

		const groupedData = myFilteredData.reduce<GroupedData>((acc, curr) => {
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
		// console.log('GROUPING: FINAL DATA ROWS:', dimensionA, dimensionB, myfinalData.length);
		return myfinalData;
	}

	function groupByDimensionsPlot(
		filteredData: DatesOverviewEntry[],
		dimensionB: string,
		metric: string
	): GroupedPlotEntry[] {
		// Step 1: Group by on_date and dimensionB
		const groupedData = filteredData.reduce<Record<string, Record<string, number>>>((acc, curr) => {
			const onDate = curr['on_date'] as string;
			const dimensionValue = curr[dimensionB] as string;
			const metricValue = (curr[metric] as number) || 0;

			// Initialize the on_date if not present
			if (!acc[onDate]) {
				acc[onDate] = {};
			}

			// Add metric value for dimensionB
			acc[onDate][dimensionValue] = (acc[onDate][dimensionValue] || 0) + metricValue;

			return acc;
		}, {});

		// Step 2: Pivot dimensionB into columns
		const pivotedData = Object.entries(groupedData).map(([on_date, dimensionValues]) => {
			return {
				on_date,
				...dimensionValues
			};
		});

		// console.log('GROUPING: FINAL PIVOTED DATA ROWS:', pivotedData);
		return pivotedData;
	}

	function formatNumber(num: number) {
		return num.toLocaleString();
	}


	onMount(() => {
		invalidate('app:dates');
	});
	

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

		<Card.Root class="xl:col-span-2">
			<Card.Header class="flex flex-row items-center">Installs by Network</Card.Header>
			<Card.Content>
				{#await data.respData}
					Loading...
				{:then plotData}
					{#if plotData.dates_overview && plotData.dates_overview.length > 0}
						<StackedBar plotData={finalPlotData}></StackedBar>
					{:else}
						Loading...
					{/if}
				{/await}
			</Card.Content>
		</Card.Root>

		<div class="gap-4 md:gap-8">
			<Card.Root class="xl:col-span-2">
				<Card.Header class="flex flex-row items-center">
					<div class="gap-2">
						<Card.Title>Overview</Card.Title>
						<Card.Description>Recent data.</Card.Description>
						<div class="flex p-2 gap-4">
							<Select.Root type="single" name="groupByA" bind:value={groupByDimA}>
								<Select.Trigger class="w-[180px]">
									{titleGroupByA}
								</Select.Trigger>
								<Select.Content>
									<Select.Group>
										<Select.GroupHeading>Group By</Select.GroupHeading>
										{#each tableDimensions as dimension}
											<Select.Item value={dimension.value} label={dimension.label}
												>{dimension.label}</Select.Item
											>
										{/each}
									</Select.Group>
								</Select.Content>
							</Select.Root>

							<Select.Root type="single" name="groupByB" bind:value={groupByDimB}>
								<Select.Trigger class="w-[180px]">
									{titleGroupByB}
								</Select.Trigger>
								<Select.Content>
									<Select.Group>
										<Select.GroupHeading>Group By</Select.GroupHeading>
										{#each tableDimensions as dimension}
											<Select.Item value={dimension.value} label={dimension.label}
												>{dimension.label}</Select.Item
											>
										{/each}
									</Select.Group>
								</Select.Content>
							</Select.Root>
						</div>
					</div>
				</Card.Header>
				<Card.Content>
					<MyOverviewTable data={finalData} {columns}></MyOverviewTable>
				</Card.Content>
			</Card.Root>
		</div>
	</main>
</div>
