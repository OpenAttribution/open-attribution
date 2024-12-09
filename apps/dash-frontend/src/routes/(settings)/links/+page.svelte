<script lang="ts">
	import { Button } from '$lib/components/ui/button/index';
	import * as Card from '$lib/components/ui/card/index';

	import { CirclePlus } from 'lucide-svelte';

	import LinksTable from '$lib/LinksTable.svelte';
	import AddClientDomainPopup from '$lib/AddClientDomainPopup.svelte';
	const { data } = $props();
</script>

<h1 class="text-2xl">Links</h1>

<h2 class="text-xl">Client Domains</h2>
<Card.Root>
	<Card.Header>
		<Card.Title>
			<div class="flex items-center">Client Domains</div>
		</Card.Title>
		<Card.Description>Manage your Client Domains and their settings.</Card.Description>
	</Card.Header>
	<Card.Content>
		<AddClientDomainPopup {data} />
		{#await data.clientDomains}
			Loading...
		{:then tableData}
			<LinksTable tableData={tableData.links} isDomains={true} />
		{/await}
	</Card.Content>
</Card.Root>

<h2 class="text-xl">Link Settings</h2>

<Card.Root>
	<Card.Header>
		<Card.Title>
			<div class="flex items-center">Links</div>
		</Card.Title>
		<Card.Description>Manage your Links and their settings.</Card.Description>
	</Card.Header>
	<Card.Content>
		<div class="flex items-center gap-2 my-4">
			<a href="links/create">
				<Button size="sm" class="h-8 gap-1">
					<CirclePlus class="h-3.5 w-3.5" />
					<span class="sr-only sm:not-sr-only sm:whitespace-nowrap">New Link</span>
				</Button>
			</a>
		</div>
		{#await data.linksData}
			Loading...
		{:then tableData}
			<LinksTable tableData={tableData.links} isDomains={false} />
		{/await}
	</Card.Content>
</Card.Root>
