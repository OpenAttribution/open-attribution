<script lang="ts">
	import Activity from 'lucide-svelte/icons/activity';
	import CreditCard from 'lucide-svelte/icons/credit-card';
	import DollarSign from 'lucide-svelte/icons/dollar-sign';
	import Users from 'lucide-svelte/icons/users';

	import SimplePlot from '$lib/components/SimplePlot.svelte';

	import { tableDimensions } from '$lib/constants';

	import OverviewTable from '$lib/my-table/OverviewTable.svelte';

	import * as Card from '$lib/components/ui/card/index.js';
	import * as Select from '$lib/components/ui/select/index.js';
	import DateRangePicker from '$lib/DateRangePicker.svelte';
	import type { MyDateRange, NetworkEntry, AppEntry, GroupedEntry } from '$types';
	import { goto } from '$app/navigation';

	import { page } from '$app/state';

	import type { OverviewEntry } from '$types';

	import { type PageData } from './$types';
	import Multiselect from '$lib/Multiselect.svelte';

	import {
		rawMetricsList,
		retainedUserMetricList,
		specialMetricsLabels,
		retentionLables,
		baseMetricsLabels
	} from '$lib/constants';

	const pageDefaultDimA = 'network_name';
	const pageDefaultDimB = 'campaign_name';

	let groupByDimA = $state(pageDefaultDimA);
	let groupByDimB = $state(pageDefaultDimB);

	interface Props {
		data: PageData;
	}

	let filteredNetworks = $state<string[]>([]);
	let filteredApps = $state<string[]>([]);

	let { data }: Props = $props();

	let filteredData = $derived(
		getFilteredData(data.respData.overview, filteredNetworks, filteredApps)
	);

	let totalImpressions = $derived(makeNewSum(filteredData, 'impressions'));
	let totalClicks = $derived(makeNewSum(filteredData, 'clicks'));
	let totalInstalls = $derived(makeNewSum(filteredData, 'installs'));
	let totalRevenue = $derived(makeNewSum(filteredData, 'revenue'));

	let tableData = $derived(
		getFinalData(
			getFilteredData(data.respData.overview, filteredNetworks, filteredApps),
			groupByDimA,
			groupByDimB
		)
	);

	function getColumns(myGroupByDimA: string, myGroupByDimB: string) {
		const columnATitle =
			tableDimensions.find((dim) => dim.value === myGroupByDimA)?.label || myGroupByDimA;
		const columnBTitle =
			tableDimensions.find((dim) => dim.value === myGroupByDimB)?.label || myGroupByDimB;

		const selectedDimensionColumns = [
			{
				accessorKey: myGroupByDimA,
				header: columnATitle,
				meta: {
					hidden: false
				}
			},
			{
				accessorKey: myGroupByDimB,
				header: columnBTitle,
				meta: {
					hidden: false
				}
			}
		];

		const metricColumns = baseMetricsLabels.map((metric) => ({
			accessorKey: metric.value,
			header: metric.label,
			meta: {
				hidden: false
			},
			cell: (props: any) => {
				const value = props.getValue();
				return value ? formatNumber(value) : '0';
			}
		}));

		const specialColumns = specialMetricsLabels.map((metric) => ({
			accessorKey: metric.value,
			header: metric.label,
			meta: { hidden: false },
			cell: (props: any) => {
				const value = props.getValue();
				return value
					? metric.value === 'ctr'
						? `${(value * 100).toFixed(2)}%`
						: formatNumber(value)
					: '0';
			}
		}));

		const retentionColumns = retentionLables.map((metric) => ({
			accessorKey: metric.value,
			header: metric.label,
			meta: {
				hidden: true
			},
			cell: (props: any) => {
				const value = props.getValue();
				return value ? `${(value * 100).toFixed(2)}%` : '0.00%';
			}
		}));

		const myCols = [
			...selectedDimensionColumns,
			...metricColumns,
			...specialColumns,
			...retentionColumns
		];
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
		let myFilteredData: OverviewEntry[] = [];
		if (myData && myData.length > 0) {
			myFilteredData = myData.filter((item) => {
				const networkMatch =
					myFilterNetworks.length === 0 || myFilterNetworks.includes(item.network);
				const appMatch = myFilterApps.length === 0 || myFilterApps.includes(item.store_id);
				return networkMatch && appMatch;
			});
		} else {
			myFilteredData = myData;
		}
		// console.log('DATA FILTER END:', myFilteredData.length);
		return myFilteredData;
	}

	function getFinalData(myData: OverviewEntry[], myGroupByDimA: string, myGroupByDimB: string) {
		let myReturnedFinalData: GroupedEntry[] = [];
		if (myData && myData.length > 0) {
			myReturnedFinalData = groupByDimensions(myData, myGroupByDimA, myGroupByDimB);
		} else {
			myReturnedFinalData = myData;
		}
		return myReturnedFinalData;
	}

	function handleNetOptions(myRows: NetworkEntry[]) {
		let myOptions;

		myOptions = myRows
			.filter((row) => row.network)
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
		filteredNetworks = event.detail;
		const params = new URLSearchParams(page.url.search);

		// Set or update the 'networks' query parameter
		// TODO I think not currently being used to check for networks!
		params.set('networks', filteredNetworks.join(','));

		// Navigate to the new URL, keeping other query parameters intact
		goto(`${page.url.pathname}?${params.toString()}`, {
			invalidateAll: true,
			replaceState: true
		});
	}

	function handleAppChange(event: CustomEvent<string[]>) {
		console.log('SELECT app options:', event.detail);
		filteredApps = event.detail;
	}

	let titleGroupByA = $derived(lookupDimensionTitle(groupByDimA));
	let titleGroupByB = $derived(lookupDimensionTitle(groupByDimB));

	function lookupDimensionTitle(dimension: string) {
		let myTitle = tableDimensions.find((dim) => dim.value === dimension)?.label || dimension;
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

		Object.values(groupedData).forEach((curr) => {
			// Calculate retention percentages
			curr['ctr'] = (curr['clicks'] as number) / curr['impressions'];
			curr['ipm'] = (curr['installs'] / curr['impressions']) * 1000;
		});

		return Object.values(groupedData);
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

		<SimplePlot {data} {filteredNetworks} {filteredApps}></SimplePlot>

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
