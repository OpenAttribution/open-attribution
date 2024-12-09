<script lang="ts">
	import { Button } from '$lib/components/ui/button/index';
	import * as Card from '$lib/components/ui/card/index';
	import * as Tabs from '$lib/components/ui/tabs';

	import { CirclePlus } from 'lucide-svelte';

	import AppsTable from '$lib/AppsTable.svelte';

	import type { PageData } from '../$types';

	const { data } = $props<{ data: PageData }>();
</script>

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
				{#await data.respData}
					Loading...
				{:then tableData}
					<AppsTable {tableData} />
				{/await}
			</Card.Content>
			<Card.Footer>
				<div class="flex items-center gap-2 my-4">
					<a href="apps/create">
						<Button size="sm" class="h-8 gap-1">
							<CirclePlus class="h-3.5 w-3.5" />
							<span class="sr-only sm:not-sr-only sm:whitespace-nowrap">New App</span>
						</Button>
					</a>
				</div>
			</Card.Footer>
		</Card.Root>
	</Tabs.Content>
</Tabs.Root>
