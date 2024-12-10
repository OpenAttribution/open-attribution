<script lang="ts">
	import * as Card from '$lib/components/ui/card/index';
	import * as Tabs from '$lib/components/ui/tabs/index';

	import AddNetwork from '$lib/AddCustomNetworkPopup.svelte';

	import { ListFilter } from 'lucide-svelte';
	import { Button } from '$lib/components/ui/button';
	import * as DropdownMenu from '$lib/components/ui/dropdown-menu';
	import { type PageData } from './$types';

	import NetworksTable from '$lib/NetworksTable.svelte';
	import CustomNetworksTable from '$lib/CustomNetworksTable.svelte';

	const { data } = $props<{ data: PageData }>();
</script>

<Tabs.Root value="all">
	<div class="flex items-center">
		<Tabs.List>
			<Tabs.Trigger value="all">All</Tabs.Trigger>
			<Tabs.Trigger value="active">Active</Tabs.Trigger>
			<Tabs.Trigger value="draft">Draft</Tabs.Trigger>
			<Tabs.Trigger value="archived" class="hidden sm:flex">Archived</Tabs.Trigger>
		</Tabs.List>
		<div class="ml-auto flex items-center gap-2">
			<DropdownMenu.Root>
				<DropdownMenu.Trigger>
					<Button variant="outline" size="sm" class="h-8 gap-1">
						<ListFilter class="h-3.5 w-3.5" />
						<span class="sr-only sm:not-sr-only sm:whitespace-nowrap"> Filter </span>
					</Button>
				</DropdownMenu.Trigger>
				<DropdownMenu.Content align="end">
					<DropdownMenu.Label>Filter by</DropdownMenu.Label>
					<DropdownMenu.Separator />
					<DropdownMenu.CheckboxItem checked>Active</DropdownMenu.CheckboxItem>
					<DropdownMenu.CheckboxItem>Draft</DropdownMenu.CheckboxItem>
					<DropdownMenu.CheckboxItem>Archived</DropdownMenu.CheckboxItem>
				</DropdownMenu.Content>
			</DropdownMenu.Root>

			<AddNetwork {data} />
		</div>
	</div>

	<Tabs.Content value="all">
		<Card.Root>
			<Card.Header>
				<Card.Title>Custom Networks</Card.Title>
				<Card.Description>Manage your custom networks & share links.</Card.Description>
			</Card.Header>
			<Card.Content>
				{#await data.respData}
					Loading...
				{:then mydata}
					<CustomNetworksTable tableData={mydata.custom_networks}></CustomNetworksTable>
				{/await}
			</Card.Content>
			<Card.Footer></Card.Footer>
		</Card.Root>

		<Card.Root>
			<Card.Header>
				<Card.Title>Networks</Card.Title>
				<Card.Description>Manage your ad network integrations.</Card.Description>
			</Card.Header>
			<Card.Content>
				{#await data.respData}
					Loading...
				{:then mydata}
					<NetworksTable tableData={mydata.networks}></NetworksTable>
				{/await}
			</Card.Content>
			<Card.Footer></Card.Footer>
		</Card.Root>
	</Tabs.Content>
</Tabs.Root>
