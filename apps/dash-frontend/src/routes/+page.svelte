<script lang="ts">
	import Activity from 'lucide-svelte/icons/activity';
	import CreditCard from 'lucide-svelte/icons/credit-card';
	import DollarSign from 'lucide-svelte/icons/dollar-sign';
	import Users from 'lucide-svelte/icons/users';

	import * as Card from '$lib/components/ui/card/index.js';
	import DateRangePicker from '$lib/DateRangePicker.svelte';
	// import type { DateRange } from 'bits-ui';
	import type { MyDateRange, OverviewEntries } from '../types';
	import { goto } from '$app/navigation';

	import type { OverviewEntry } from '../types';

	import { type PageData } from './$types';
	import OverviewTable from '$lib/OverviewTable.svelte';
	import Multiselect from '$lib/Multiselect.svelte';

	const { data } = $props<{ data: PageData }>();

	function makeSum(newData: OverviewEntries, property: keyof OverviewEntry) {
		if (newData && newData.length > 0) {
			console.log('isthisworking');
			return newData.reduce((total: number, entry: OverviewEntry) => {
				const value = entry[property];
				return total + (typeof value === 'number' ? value : 0);
			}, 0);
		} else {
			console.log('NOPE');
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

	let overviewData = $state(data.respData.overview);

	// let networks = $state(data.networks);
	// let apps = $state(data.apps);

	// const netOptions = networks.map((network) => ({
	// 	value: network.name,
	// 	label: network.name
	// }));

	function handleMakeOptions(myRows: { name: string }[], myType: string) {
		let myOptions;

		if (myType === 'networks') {
			myOptions = myRows.map((row) => ({
				value: row.name,
				label: row.name
			}));
		}

		if (myType === 'apps') {
			// Fixing the second condition to check for apps
			myOptions = myRows.map((app) => ({
				value: app.name,
				label: app.name
			}));
		}

		return myOptions || []; // Ensure we return an empty array if no condition is met
	}

	function handleChange(event: CustomEvent<string[]>) {
		console.log('Selected options:', event.detail);
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
								options={handleMakeOptions(myapps.apps, 'apps')}
								placeholder="Filter by App"
								on:change={handleChange}
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
								options={handleMakeOptions(mynets.networks, 'networks')}
								placeholder="Filter by Network"
								on:change={handleChange}
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
						<OverviewTable overviewData={mydata.overview}></OverviewTable>
					{/await}
				</Card.Content>
			</Card.Root>
		</div>
	</main>
</div>
