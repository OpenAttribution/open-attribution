<script lang="ts">
	import Activity from 'lucide-svelte/icons/activity';
	import CreditCard from 'lucide-svelte/icons/credit-card';
	import DollarSign from 'lucide-svelte/icons/dollar-sign';
	import Users from 'lucide-svelte/icons/users';

	import * as Card from '$lib/components/ui/card/index.js';
	import DateRangePicker from '$lib/DateRangePicker.svelte';
	import type { MyDateRange, OverviewEntries, NetworkEntry, AppEntry } from '../types';
	import { goto } from '$app/navigation';

	import type { OverviewEntry } from '../types';

	import { type PageData } from './$types';
	import OverviewTable from '$lib/OverviewTable.svelte';
	import Multiselect from '$lib/Multiselect.svelte';

	const { data } = $props<{ data: PageData }>();

	function makeSum(newData: OverviewEntries, property: keyof OverviewEntry) {
		if (newData && newData.length > 0) {
			return newData.reduce((total: number, entry: OverviewEntry) => {
				const value = entry[property];
				return total + (typeof value === 'number' ? value : 0);
			}, 0);
		} else {
			console.log('makeSum not working!');
			return 0;
		}
	}

	let totalImpressions = $state(0);

	function makeNewSum(newData: OverviewEntries) {
		if (newData && newData.length > 0) {
			totalImpressions = newData.reduce((total: number, entry: OverviewEntry) => {
				const value = entry['impressions'];
				return total + (typeof value === 'number' ? value : 0);
			}, 0);
		} else {
			console.log('makeSum not working!');
			return 0;
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

	let filterNetworks = $state([]);
	let filterApps = $state([]);

	let overviewData = $state(data.respData.overview);
	let filteredData = $state(getFilteredData(data.respData.overview));

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

	function handleNetOptions(myRows: NetworkEntry[]) {
		let myOptions;

		myOptions = myRows.map((row) => ({
			value: row.postback_id,
			label: row.name
		}));
		return myOptions;
	}

	function handleAppOptions(myRows: AppEntry[], myType: string) {
		let myOptions;

		// Fixing the second condition to check for apps
		myOptions = myRows.map((app) => ({
			value: app.store_id,
			label: app.name
		}));
		return myOptions;
	}

	function handleNetChange(event: CustomEvent<string[]>) {
		console.log('Selected net options:', event.detail);
		filterNetworks = event.detail;
	}

	function handleAppChange(event: CustomEvent<string[]>) {
		console.log('Selected app options:', event.detail);
		filterApps = event.detail;
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
					{#await data.respApps}
						Loading...
					{:then myapps}
						{#if myapps.apps && myapps.apps.length > 0}
							<Multiselect
								options={handleAppOptions(myapps.apps, 'apps')}
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
					{#await data.respNets}
						Loading...
					{:then mynets}
						{#if mynets.networks && mynets.networks.length > 0}
							<Multiselect
								options={handleNetOptions(mynets.networks)}
								placeholder="Filter by Network"
								on:change={handleNetChange}
							/>
						{:else}
							No networks.
						{/if}
					{/await}

					<!-- {#await data.apps}
						Loading...
					{:then myapps}
						<Multiselect
							options={handleMakeOptions(myapps)}
							placeholder="Select Types..."
							on:change={handleChange}
						/>
					{/await} -->
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
						<div class="text-2xl font-bold">{totalImpressions}</div>
						<p class="text-muted-foreground text-xs">+19% from last month?</p>
					</Card.Content>
					X
					<Card.Content>
						<div class="text-2xl font-bold">{makeSum(mydatas.overview, 'impressions')}</div>
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
						<div class="text-2xl font-bold">{makeSum(mydatas.overview, 'clicks')}</div>
						<p class="text-muted-foreground text-xs">
							{#if makeSum(mydatas.overview, 'impressions') > 0}
								{(
									(makeSum(mydatas.overview, 'clicks') / makeSum(mydatas.overview, 'impressions')) *
									100
								).toFixed(2)}%
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
							{makeSum(mydatas.overview, 'impressions')}
						</div>
						<p class="text-muted-foreground text-xs">
							{#if makeSum(mydatas.overview, 'impressions') > 0}
								{(
									makeSum(mydatas.overview, 'installs') /
									(makeSum(mydatas.overview, 'impressions') / 1000)
								).toFixed(2)}
								% Installs Per Mille
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
							{makeSum(mydatas.overview, 'revenue').toLocaleString('en-US', {
								style: 'currency',
								currency: 'USD'
							})}
						</div>
						<p class="text-muted-foreground text-xs">+19% from last month</p>
					</Card.Content>
				{/await}
			</Card.Root>
		</div>

		<div class="gap-4 md:gap-8">
			<Card.Root class="xl:col-span-2">
				<Card.Header class="flex flex-row items-center">
					<div class="gap-2">
						<Card.Title>My Table</Card.Title>
						<Card.Description>Recent data.</Card.Description>
					</div>
				</Card.Header>
				<Card.Content>
					{#await data.respData}
						Loading...
					{:then mydata}
						{#if mydata.overview && mydata.overview.length > 0}
							{getFilteredData(mydata.overview)}
							<!-- <OverviewTable overviewData={getFilteredData(mydata.overview)}></OverviewTable> -->
							<OverviewTable overviewData={filteredData}></OverviewTable>
						{:else}
							Loading...
						{/if}
					{/await}
				</Card.Content>
			</Card.Root>
		</div>
	</main>
</div>
