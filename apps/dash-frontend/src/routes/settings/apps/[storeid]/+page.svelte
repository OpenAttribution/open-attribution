<script lang="ts">
	import { Button } from '$lib/components/ui/button/index';
	import * as Card from '$lib/components/ui/card/index';
	import * as Tabs from '$lib/components/ui/tabs';
	import { page } from '$app/stores';
	import { CirclePlus } from 'lucide-svelte';
	import AppLinksTable from '$lib/AppLinksTable.svelte';

	let { data } = $props();
</script>

{#await data.appData}
	loading ...
{:then app}
	{console.log(app)}
	<h1>App: {app.app.name}</h1>
	<h1>StoreId: {app.app.store_id}</h1>
	<h1>Store: {app.app.store}</h1>
	<h1>Created: {app.app.created_at}</h1>
	<h2 class="h2">App: {$page.params.storeid}</h2>
{:catch}
	<h1>App: Not Found</h1>
	}
{/await}

<h1 class="text-2xl">App Settings</h1>

<Tabs.Root value="all">
	<Tabs.Content value="all">
		<Card.Root>
			<Card.Header>
				<Card.Title>
					<div class="flex items-center">Apps</div>
				</Card.Title>
				<Card.Description>Manage your Apps and their settings.</Card.Description>
			</Card.Header>
			<Card.Content>
				{#await data.appLinks}
					Loading...
				{:then appLinks}
					<AppLinksTable {appLinks} />
				{/await}
			</Card.Content>
			<Card.Footer>
				<div class="flex items-center gap-2 my-4">
					<a href="/settings/apps/{$page.params.storeid}/createlink">
						<Button size="sm" class="h-8 gap-1">
							<CirclePlus class="h-3.5 w-3.5" />
							<span class="sr-only sm:not-sr-only sm:whitespace-nowrap">New Link</span>
						</Button>
					</a>
				</div>
			</Card.Footer>
		</Card.Root>
	</Tabs.Content>
</Tabs.Root>
