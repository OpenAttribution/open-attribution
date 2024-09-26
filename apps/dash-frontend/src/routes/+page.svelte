<script lang="ts">
	import Activity from 'lucide-svelte/icons/activity';
	import CircleUser from 'lucide-svelte/icons/circle-user';
	import CreditCard from 'lucide-svelte/icons/credit-card';
	import DollarSign from 'lucide-svelte/icons/dollar-sign';
	import Menu from 'lucide-svelte/icons/menu';
	import Package2 from 'lucide-svelte/icons/package-2';
	import Search from 'lucide-svelte/icons/search';
	import Users from 'lucide-svelte/icons/users';

	import { Button } from '$lib/components/ui/button/index.js';
	import * as Card from '$lib/components/ui/card/index.js';
	import * as DropdownMenu from '$lib/components/ui/dropdown-menu/index.js';
	import { Input } from '$lib/components/ui/input/index.js';
	import * as Sheet from '$lib/components/ui/sheet/index.js';
	import * as Table from '$lib/components/ui/table/index.js';
	import DateRangePicker from '$lib/DateRangePicker.svelte';
	import type { DateRange } from 'bits-ui';
	import { goto } from '$app/navigation';

	let myRange: DateRange | undefined = undefined;

	function handleDateChange(newRange: DateRange | undefined) {
		myRange = newRange;
		// console.log(dateRange);

		if (newRange && newRange.start && newRange.end) {
			// Format the dates as needed (ISO strings or other formats)
			const startDate = newRange.start.toString(); // Adjust as necessary
			const endDate = newRange.end.toString(); // Adjust as necessary

			// Navigate to the same page with query parameters for start and end dates
			goto(`?start=${startDate}&end=${endDate}`);
		}
	}
</script>

<div class="flex min-h-screen w-full flex-col">
	<header class="bg-background sticky top-0 flex h-16 items-center gap-4 border-b px-4 md:px-6">
		<nav
			class="hidden flex-col gap-6 text-lg font-medium md:flex md:flex-row md:items-center md:gap-5 md:text-sm lg:gap-6"
		>
			<a href="##" class="flex items-center gap-2 text-lg font-semibold md:text-base">
				<Package2 class="h-6 w-6" />
				<span class="sr-only">Acme Inc</span>
			</a>
			<a href="##" class="text-foreground hover:text-foreground transition-colors"> Dashboard </a>
			<a href="##" class="text-muted-foreground hover:text-foreground transition-colors">
				Orders
			</a>
			<a href="##" class="text-muted-foreground hover:text-foreground transition-colors">
				Products
			</a>
			<a href="##" class="text-muted-foreground hover:text-foreground transition-colors">
				Customers
			</a>
			<a href="##" class="text-muted-foreground hover:text-foreground transition-colors">
				Analytics
			</a>
		</nav>
		<Sheet.Root>
			<Sheet.Trigger asChild let:builder>
				<Button variant="outline" size="icon" class="shrink-0 md:hidden" builders={[builder]}>
					<Menu class="h-5 w-5" />
					<span class="sr-only">Toggle navigation menu</span>
				</Button>
			</Sheet.Trigger>
			<Sheet.Content side="left">
				<nav class="grid gap-6 text-lg font-medium">
					<a href="##" class="flex items-center gap-2 text-lg font-semibold">
						<Package2 class="h-6 w-6" />
						<span class="sr-only">Acme Inc</span>
					</a>
					<a href="##" class="hover:text-foreground"> Dashboard </a>
					<a href="##" class="text-muted-foreground hover:text-foreground"> Orders </a>
					<a href="##" class="text-muted-foreground hover:text-foreground"> Products </a>
					<a href="##" class="text-muted-foreground hover:text-foreground"> Customers </a>
					<a href="##" class="text-muted-foreground hover:text-foreground"> Analytics </a>
				</nav>
			</Sheet.Content>
		</Sheet.Root>
		<div class="flex w-full items-center gap-4 md:ml-auto md:gap-2 lg:gap-4">
			<form class="ml-auto flex-1 sm:flex-initial">
				<div class="relative">
					<Search class="text-muted-foreground absolute left-2.5 top-2.5 h-4 w-4" />
					<Input
						type="search"
						placeholder="Search products..."
						class="pl-8 sm:w-[300px] md:w-[200px] lg:w-[300px]"
					/>
				</div>
			</form>
			<DropdownMenu.Root>
				<DropdownMenu.Trigger asChild let:builder>
					<Button builders={[builder]} variant="secondary" size="icon" class="rounded-full">
						<CircleUser class="h-5 w-5" />
						<span class="sr-only">Toggle user menu</span>
					</Button>
				</DropdownMenu.Trigger>
				<DropdownMenu.Content align="end">
					<DropdownMenu.Label>My Account</DropdownMenu.Label>
					<DropdownMenu.Separator />
					<DropdownMenu.Item>Settings</DropdownMenu.Item>
					<DropdownMenu.Item>Support</DropdownMenu.Item>
					<DropdownMenu.Separator />
					<DropdownMenu.Item>Logout</DropdownMenu.Item>
				</DropdownMenu.Content>
			</DropdownMenu.Root>
		</div>
	</header>
	<main class="flex flex-1 flex-col gap-4 p-4 md:gap-8 md:p-8">
		<DateRangePicker onChange={handleDateChange} />
		{#if myRange && myRange.start && myRange.end}
			<p>
				Selected Start Date: {myRange.start.toString()} <br />
				Selected End Date: {myRange.end.toString()}
			</p>
		{/if}
		<div class="grid gap-4 md:grid-cols-2 md:gap-8 lg:grid-cols-4">
			<Card.Root>
				<Card.Header class="flex flex-row items-center justify-between space-y-0 pb-2">
					<Card.Title class="text-sm font-medium">Total Revenue</Card.Title>
					<DollarSign class="text-muted-foreground h-4 w-4" />
				</Card.Header>
				<Card.Content>
					<div class="text-2xl font-bold">$45,231.89</div>
					<p class="text-muted-foreground text-xs">+20.1% from last month</p>
				</Card.Content>
			</Card.Root>
			<Card.Root>
				<Card.Header class="flex flex-row items-center justify-between space-y-0 pb-2">
					<Card.Title class="text-sm font-medium">Subscriptions</Card.Title>
					<Users class="text-muted-foreground h-4 w-4" />
				</Card.Header>
				<Card.Content>
					<div class="text-2xl font-bold">+2350</div>
					<p class="text-muted-foreground text-xs">+180.1% from last month</p>
				</Card.Content>
			</Card.Root>
			<Card.Root>
				<Card.Header class="flex flex-row items-center justify-between space-y-0 pb-2">
					<Card.Title class="text-sm font-medium">Sales</Card.Title>
					<CreditCard class="text-muted-foreground h-4 w-4" />
				</Card.Header>
				<Card.Content>
					<div class="text-2xl font-bold">+12,234</div>
					<p class="text-muted-foreground text-xs">+19% from last month</p>
				</Card.Content>
			</Card.Root>
			<Card.Root>
				<Card.Header class="flex flex-row items-center justify-between space-y-0 pb-2">
					<Card.Title class="text-sm font-medium">Active Now</Card.Title>
					<Activity class="text-muted-foreground h-4 w-4" />
				</Card.Header>
				<Card.Content>
					<div class="text-2xl font-bold">+573</div>
					<p class="text-muted-foreground text-xs">+201 since last hour</p>
				</Card.Content>
			</Card.Root>
		</div>
		<div class="gap-4 md:gap-8">
			<Card.Root class="xl:col-span-2">
				<Card.Header class="flex flex-row items-center">
					<div class="gap-2">
						<Card.Title>Campaign</Card.Title>
						<Card.Description>Recent data.</Card.Description>
					</div>
				</Card.Header>
				<Card.Content>
					<Table.Root>
						<Table.Header>
							<Table.Row>
								<Table.Head>Network</Table.Head>
								<Table.Head class="xl:table.-column">Campaign</Table.Head>
								<Table.Head class="xl:table.-column">Impressions</Table.Head>
								<Table.Head class="xl:table.-column">Clicks</Table.Head>
								<Table.Head class="">Installs</Table.Head>
							</Table.Row>
						</Table.Header>
						<Table.Body>
							<Table.Row>
								<Table.Cell>
									<div class="font-medium">networkA</div>
								</Table.Cell>
								<Table.Cell class="">campaignA</Table.Cell>
								<Table.Cell class="">4000</Table.Cell>
								<Table.Cell class="">200</Table.Cell>
								<Table.Cell class="">2</Table.Cell>
							</Table.Row>
							<Table.Row>
								<Table.Cell>
									<div class="font-medium">networkA</div>
								</Table.Cell>
								<Table.Cell class="">campaignA</Table.Cell>
								<Table.Cell class="">3000</Table.Cell>
								<Table.Cell class="">300</Table.Cell>
								<Table.Cell class="">3</Table.Cell>
							</Table.Row>
						</Table.Body>
					</Table.Root>
				</Card.Content>
			</Card.Root>
		</div>
	</main>
</div>
