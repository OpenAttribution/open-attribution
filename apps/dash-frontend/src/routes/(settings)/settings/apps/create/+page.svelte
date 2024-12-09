<script lang="ts">
	import * as Card from '$lib/components/ui/card/index';
	import * as Tabs from '$lib/components/ui/tabs';

	import type { PageData } from '../$types';

	const { data } = $props<{ data: PageData }>();

	import AddApp from './AddApp.svelte';
</script>

<h1 class="text-2xl">Create New App</h1>

<Tabs.Root value="all">
	<Tabs.Content value="all">
		<Card.Root>
			<Card.Header>
				<Card.Description>Setup your app. There is one per store.</Card.Description>
			</Card.Header>
			<Card.Content>
				<AddApp data={data.form} />
			</Card.Content>
			<Card.Footer></Card.Footer>
		</Card.Root>
	</Tabs.Content>
</Tabs.Root>
