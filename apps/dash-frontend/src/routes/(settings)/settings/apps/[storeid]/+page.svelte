<script lang="ts">
	import { Button } from '$lib/components/ui/button/index';
	import * as Card from '$lib/components/ui/card/index';
	import { page } from '$app/stores';
	import { CirclePlus } from 'lucide-svelte';
	import AppLinksTable from '$lib/LinksTable.svelte';
	import { format } from 'date-fns';

	import IconAndroid from '$lib/svg/IconAndroid.svelte';
	import IconIOS from '$lib/svg/IconiOS.svelte';

	let { data } = $props();
</script>

<h1 class="text-2xl">App Settings</h1>

<Card.Root>
	{#await data.appData}
		loading ...
	{:then app}
		<Card.Header>
			<Card.Title>
				<span class="flex items-center gap-2">
					{#if app.app.store == 1}
						<IconAndroid size="40" />
					{:else if app.app.store === 2}
						<IconIOS size="50" />
					{:else}
						MissingStoreIcon
					{/if}
					{app.app.name}
				</span>
			</Card.Title>
			<Card.Description>
				<div class="flex flex-col-2">
					<span class="flex-1">Manage your App's settings and custom share links.</span>
					<div class="flex flex-col">
						<span>Store ID: {app.app.store_id} </span><span>
							Created: {format(app.app.created_at, 'yyyy-MM-dd')}</span
						>
					</div>
				</div>
			</Card.Description>
		</Card.Header>
	{:catch}
		<h1>App: Not Found</h1>
		}
	{/await}

	<Card.Content></Card.Content>
	<Card.Footer></Card.Footer>
</Card.Root>

<Card.Root>
	<Card.Header>
		<Card.Title>App Links</Card.Title>
	</Card.Header>
	<Card.Content>
		<div class="flex items-center gap-2 my-4">
			<a href="/settings/apps/{$page.params.storeid}/createlink">
				<Button size="sm" class="h-8 gap-1">
					<CirclePlus class="h-3.5 w-3.5" />
					<span class="sr-only sm:not-sr-only sm:whitespace-nowrap">New Link</span>
				</Button>
			</a>
		</div>

		{#await data.appLinks}
			Loading...
		{:then appLinks}
			<AppLinksTable tableData={appLinks.links} isDomains={false} />
		{/await}
	</Card.Content>
</Card.Root>
