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

	const { data } = $props<{ data: PageData }>();

	function handleUpdate(newData: OverviewEntries) {
		if (newData && newData.length > 0) {
			console.log('isthisworking');
			return newData.reduce((total: number, entry: OverviewEntry) => total + entry.clicks, 0);
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

	let totalClicks = $state(handleUpdate(data.respData.overview));



	let totalRevenue = $derived.by(() => {
		// Check if overviewData is defined and not null
		if (overviewData && overviewData.length > 0) {
			return overviewData.reduce((acc: number, entry: OverviewEntry) => acc + entry.revenue, 0);
		} else {
			return 0;
		}
	});

	let totalImpressions = $derived.by(() => {
		let total = 0;
		if (overviewData && overviewData.length > 0) {
			total = overviewData.reduce(
				(acc: number, entry: OverviewEntry) => acc + entry.impressions,
				0
			);
		}
		return total;
	});

	// let totalClicks = $state(overviewData.reduce((acc, entry) => acc + entry.clicks, 0));
	// totalClicks = 0;

	// Updating overviewData will automatically recalculate totalClicks
	function updateData() {
		overviewData = [{ clicks: 20 }, { clicks: 30 }];
	}

	let totalInstalls = $derived.by(() => {
		if (overviewData && Array.isArray(overviewData)) {
			return overviewData.reduce((acc: number, entry: OverviewEntry) => acc + entry.installs, 0);
		} else {
			return 0;
		}
	});

	let formattedRevenue = $derived.by(() => {
		return totalRevenue.toLocaleString('en-US', {
			style: 'currency',
			currency: 'USD'
		});
	});
</script>

<div class="flex min-h-screen w-full flex-col">
	
	<main class="flex flex-1 flex-col gap-4 p-4 md:gap-8 md:p-8">
		<DateRangePicker onChange={handleDateChange} />
		<div class="grid gap-4 md:grid-cols-2 md:gap-8 lg:grid-cols-4">
			<Card.Root>
				<Card.Header class="flex flex-row items-center justify-between space-y-0 pb-2">
					<Card.Title class="text-sm font-medium">Impressions</Card.Title>
					<Users class="text-muted-foreground h-4 w-4" />
				</Card.Header>
				<Card.Content>
					<div class="text-2xl font-bold">{totalImpressions}</div>
					<p class="text-muted-foreground text-xs">+180.1% from last month</p>
				</Card.Content>
			</Card.Root>
			<Card.Root>
				<Card.Header class="flex flex-row items-center justify-between space-y-0 pb-2">
					<Card.Title class="text-sm font-medium">Clicks</Card.Title>
					<CreditCard class="text-muted-foreground h-4 w-4" />
				</Card.Header> {totalClicks} ->>
				{#await data.respData}
					Loading...
				{:then mydatas}
					<Card.Content>
						<div class="text-2xl font-bold">{handleUpdate(mydatas)}</div>
						<p class="text-muted-foreground text-xs">+19% from last month</p>
					</Card.Content>
				{/await}
			</Card.Root>
			<Card.Root>
				<Card.Header class="flex flex-row items-center justify-between space-y-0 pb-2">
					<Activity class="text-muted-foreground h-4 w-4" />
				Installs 	
				</Card.Header>
				<Card.Content>
					<div class="text-2xl font-bold">{totalInstalls}</div>
					<p class="text-muted-foreground text-xs">+201 since last hour</p>
				</Card.Content>
			</Card.Root>
			<Card.Root>
				<Card.Header class="flex flex-row items-center justify-between space-y-0 pb-2">
					<Card.Title class="text-sm font-medium">Total Revenue</Card.Title>
					<DollarSign class="text-muted-foreground h-4 w-4" />
				</Card.Header>
				<Card.Content>
					<div class="text-2xl font-bold">{totalRevenue} -> {formattedRevenue}</div>
					<p class="text-muted-foreground text-xs">+20.1% from last month</p>
				</Card.Content>
			</Card.Root>
		</div>

		<div class="gap-4 md:gap-8">
			<Card.Root class="xl:col-span-2">
				<Card.Header class="flex flex-row items-center">
					<div class="gap-2">
						<Card.Title>Campaign Shadcn Table</Card.Title>
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
