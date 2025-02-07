<script lang="ts">
	import Activity from 'lucide-svelte/icons/activity';
	import CreditCard from 'lucide-svelte/icons/credit-card';
	import DollarSign from 'lucide-svelte/icons/dollar-sign';
	import Users from 'lucide-svelte/icons/users';

	import { tableDimensions } from '$lib/constants';

	import OverviewTable from '$lib/my-table/OverviewTable.svelte';

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
	} from '$types';
	import { goto } from '$app/navigation';

	import StackedBar from '$lib/components/mycharts/StackedBarChart.svelte';

	import { page } from '$app/state';

	import type { OverviewEntry } from '$types';

	import { type PageData } from './$types';
	import Multiselect from '$lib/Multiselect.svelte';

	import {
		rawMetricsList,
		retainedUserMetricList,
		retentionLables,
		baseMetricsLabels
	} from '$lib/constants';

	const pageDefaultDimA = 'network_name';
	const pageDefaultDimB = 'campaign_name';
	const pageDefaultPlotBarMetric = 'installs';
	const pageDefaultPlotLineMetric = 'impressions';

	let groupByDimA = $state(pageDefaultDimA);
	let groupByDimB = $state(pageDefaultDimB);
	// let plotBarBy = $state(pageDefaultDimA);
	let plotBarMetric = $state(pageDefaultPlotBarMetric);
	let plotLineMetric = $state(pageDefaultPlotLineMetric);

	interface Props {
		data: PageData;
	}

	let filterNetworks = $state<string[]>([]);
	let filterApps = $state<string[]>([]);

	let { data }: Props = $props();

	let filteredData = $derived(getFilteredData(data.respData.overview, filterNetworks, filterApps));

	let totalImpressions = $derived(makeNewSum(filteredData, 'impressions'));
	let totalClicks = $derived(makeNewSum(filteredData, 'clicks'));
	let totalInstalls = $derived(makeNewSum(filteredData, 'installs'));
	let totalRevenue = $derived(makeNewSum(filteredData, 'revenue'));

	let tableData = $derived(
		getFinalData(
			getFilteredData(data.respData.overview, filterNetworks, filterApps),
			groupByDimA,
			groupByDimB
		)
	);

	let finalBarPlotData = $derived(
		getFinalPlotData(
			getFilteredPlotData(data.respData.dates_overview, filterNetworks, filterApps),
			groupByDimA,
			plotBarMetric
		)
	);

	let finalLinePlotData = $derived(
		getFinalPlotData(
			getFilteredPlotData(data.respData.dates_overview, filterNetworks, filterApps),
			groupByDimA,
			plotLineMetric
		)
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

		// Add the metric columns
		const metricColumns = baseMetricsLabels.map((metric) => ({
			accessorKey: metric.value,
			header: metric.label,
			cell: (props: any) => {
				const value = props.getValue();
				return value ? formatNumber(value) : '0';
			}
		}));

		const retentionColumns = retentionLables.map((metric) => ({
			accessorKey: metric.value,
			header: metric.label,
			visible: false,
			cell: (props: any) => {
				const value = props.getValue();
				return value ? `${(value * 100).toFixed(2)}%` : '0.00%';
			}
		}));

		// const myCols = [...selectedDimensionColumns, ...remainingDimensionColumns, ...metricColumns];
		const myCols = [...selectedDimensionColumns, ...metricColumns, ...retentionColumns];
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

	function getFinalPlotData(
		myData: DatesOverviewEntry[],
		groupByKey: string = 'network',
		metric: string = 'installs'
	) {
		let myReturnedFinalPlotData: GroupedPlotEntry[] = [];
		if (myData && myData.length > 0) {
			myReturnedFinalPlotData = groupByDimensionsPlot(myData, groupByKey, metric);
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
		const params = new URLSearchParams(page.url.search);

		// Set or update the 'networks' query parameter
		// TODO I think not currently being used to check for networks!
		params.set('networks', filterNetworks.join(','));

		// Navigate to the new URL, keeping other query parameters intact
		goto(`${page.url.pathname}?${params.toString()}`, {
			invalidateAll: true,
			replaceState: true
		});
	}

	function handleAppChange(event: CustomEvent<string[]>) {
		console.log('SELECT app options:', event.detail);
		filterApps = event.detail;
	}

	let titleGroupByA = $derived(lookupDimensionTitle(groupByDimA));
	let titleGroupByB = $derived(lookupDimensionTitle(groupByDimB));

	let titleBarMetric = $derived(lookupMetricTitle(plotBarMetric));
	let titleLineMetric = $derived(lookupMetricTitle(plotLineMetric));

	function lookupDimensionTitle(dimension: string) {
		let myTitle = tableDimensions.find((dim) => dim.value === dimension)?.label || dimension;
		return myTitle;
	}

	function lookupMetricTitle(metric: string) {
		let myTitle = baseMetricsLabels.find((m) => m.value === metric)?.label || metric;
		return myTitle;
	}

	interface GroupedData {
		[groupKey: string]: GroupedEntry;
	}

	function groupByDimensions(
		myFilteredData: OverviewEntry[],
		dimensionA: string,
		dimensionB: string
	) {
		let groupedData = myFilteredData.reduce<GroupedData>((acc, curr) => {
			const keyA = curr[dimensionA] as string;
			const keyB = curr[dimensionB] as string;
			const groupKey = `${keyA}|${keyB}`;

			if (!acc[groupKey]) {
				// Create initial object with dimensions
				acc[groupKey] = {
					[dimensionA]: keyA,
					[dimensionB]: keyB
				} as GroupedEntry;

				// Initialize all metrics to 0
				rawMetricsList.forEach((metric) => {
					acc[groupKey][metric] = 0;
				});
			}

			// Sum up all metrics
			rawMetricsList.forEach((metric) => {
				acc[groupKey][metric] = (acc[groupKey][metric] as number) + ((curr[metric] as number) || 0);
			});

			return acc;
		}, {});

		Object.values(groupedData).forEach((curr) => {
			// Calculate retention percentages
			retainedUserMetricList.forEach((metric) => {
				curr['ret_' + metric] = (curr[metric] as number) / curr['installs'];
			});
		});

		return Object.values(groupedData);
	}

	function groupByForBasicMetric(
		myFilteredData: OverviewEntry[],
		dimension: string,
		metric: string
	) {
		return myFilteredData.reduce<Record<string, Record<string, number>>>((acc, curr) => {
			const onDate = curr['on_date'] as string;
			const dimensionValue = curr[dimension] as string;
			const metricValue = (curr[metric] as number) || 0;

			// Initialize the on_date if not present
			if (!acc[onDate]) {
				acc[onDate] = {};
			}

			// Add metric value for dimension
			acc[onDate][dimensionValue] = (acc[onDate][dimensionValue] || 0) + metricValue;

			return acc;
		}, {});
	}

	function groupByForComplexMetric(
		myFilteredData: OverviewEntry[],
		dimension: string,
		metric: string
	) {
		// Remove 'ret_' prefix from metric name, so we can use it as a dimension
		const dx_metric = metric.replace('ret_', '');

		// First, group by date and dimension, summing any flat metrics
		const grouped = myFilteredData.reduce<{
			[date: string]: {
				[dimension: string]: {
					metricSum: number;
					installsSum: number;
				};
			};
		}>((acc, curr) => {
			const onDate = curr.on_date;
			const dimensionValue = curr[dimension] as string;
			const metricValue = (curr[dx_metric] as number) || 0;
			const installsValue = curr.installs || 0;

			// Initialize nested objects if they don't exist
			if (!acc[onDate]) {
				acc[onDate] = {};
			}
			if (!acc[onDate][dimensionValue]) {
				acc[onDate][dimensionValue] = {
					metricSum: 0,
					installsSum: 0
				};
			}

			// Sum up the values
			acc[onDate][dimensionValue].metricSum += metricValue;
			acc[onDate][dimensionValue].installsSum += installsValue;

			return acc;
		}, {});

		// Calculate final metrics by dividing sums
		const result: Record<string, Record<string, number>> = {};

		for (const date in grouped) {
			result[date] = {};
			for (const dim in grouped[date]) {
				const { metricSum, installsSum } = grouped[date][dim];
				result[date][dim] = installsSum > 0 ? metricSum / installsSum : 0;
			}
		}

		return result;
	}

	function groupByDimensionsPlot(
		filteredData: DatesOverviewEntry[],
		dimension: string,
		metric: string
	): GroupedPlotEntry[] {
		const userStartDate = page.url.searchParams.get('start') || '';
		const userEndDate = page.url.searchParams.get('end') || '';

		let startDate = '';
		let endDate = '';

		if (userStartDate && userStartDate < filteredData[0]['on_date']) {
			startDate = userStartDate;
		} else {
			startDate = filteredData[0]['on_date'] as string;
		}

		if (userEndDate && userEndDate > filteredData[filteredData.length - 1]['on_date']) {
			endDate = userEndDate;
		} else {
			endDate = filteredData[filteredData.length - 1]['on_date'] as string;
		}

		// Generate array of all dates between start and end
		const dates: string[] = [];
		const currentDate = new Date(startDate);
		const lastDate = new Date(endDate);

		while (currentDate <= lastDate) {
			dates.push(currentDate.toISOString().split('T')[0]);
			currentDate.setDate(currentDate.getDate() + 1);
		}

		let groupedData: Record<string, Record<string, number>> = {};
		if (metric.startsWith('ret_')) {
			groupedData = groupByForComplexMetric(filteredData, dimension, metric);
			console.log('groupedData=', groupedData);
		} else {
			groupedData = groupByForBasicMetric(filteredData, dimension, metric);
		}

		// Step 1: Group by on_date and dimension SINGLE metric

		// Step 2: Ensure all dates exist in groupedData with zero values
		const allDimensionValues = new Set<string>();
		Object.values(groupedData).forEach((dimensionValues) => {
			Object.keys(dimensionValues).forEach((dim) => allDimensionValues.add(dim));
		});

		// Create complete dataset with all dates
		const completeData = dates.reduce<Record<string, Record<string, number>>>((acc, date) => {
			acc[date] = acc[date] || {};
			// Initialize all dimension values to 0 for this date
			allDimensionValues.forEach((dim) => {
				acc[date][dim] = groupedData[date]?.[dim] || 0;
			});
			return acc;
		}, {});

		// Step 3: Pivot dimension into columns
		const pivotedData = Object.entries(completeData).map(([on_date, dimensionValues]) => {
			return {
				on_date,
				...dimensionValues
			};
		});

		return pivotedData.sort((a, b) => a.on_date.localeCompare(b.on_date));
	}

	function formatNumber(num: number) {
		return num.toLocaleString();
	}

	function handleDateChange(newRange: MyDateRange | undefined) {
		if (newRange && newRange.start && newRange.end) {
			const startDate = newRange.start.toString();
			const endDate = newRange.end.toString();

			goto(`?start=${startDate}&end=${endDate}`);
		}
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
			<Card.Header class="flex flex-row items-center">
				<div class="flex flex-row items-center gap-2">
					<Select.Root type="single" name="plotBarBy" bind:value={groupByDimA}>
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
					<Select.Root type="single" name="plotBarMetric" bind:value={plotBarMetric}>
						<Select.Trigger class="w-[180px]">
							{titleBarMetric}
						</Select.Trigger>
						<Select.Content>
							<Select.Group>
								<Select.GroupHeading>Metric</Select.GroupHeading>
								{#each baseMetricsLabels as metric}
									<Select.Item value={metric.value} label={metric.label}>{metric.label}</Select.Item
									>
								{/each}
							</Select.Group>
						</Select.Content>
					</Select.Root>
					<Select.Root type="single" name="plotLineMetric" bind:value={plotLineMetric}>
						<Select.Trigger class="w-[180px]">
							{titleLineMetric}
						</Select.Trigger>
						<Select.Content>
							<Select.Group>
								<Select.GroupHeading>Metric</Select.GroupHeading>
								{#each [...baseMetricsLabels, ...retentionLables] as metric}
									<Select.Item value={metric.value} label={metric.label}>{metric.label}</Select.Item
									>
								{/each}
							</Select.Group>
						</Select.Content>
					</Select.Root>
				</div>
			</Card.Header>

			<Card.Content>
				{#await data.respData}
					Loading...
				{:then plotData}
					{#if plotData.dates_overview && plotData.dates_overview.length > 0}
						<StackedBar plotData={finalBarPlotData} lineData={finalLinePlotData}></StackedBar>
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
					<OverviewTable data={tableData} {columns}></OverviewTable>
				</Card.Content>
			</Card.Root>
		</div>
	</main>
</div>
