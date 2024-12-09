<script lang="ts">
	import * as Card from '$lib/components/ui/card/index';
	import * as Tabs from '$lib/components/ui/tabs';
	import type { PageData } from '../$types';

	const { data } = $props<{ data: PageData }>();

	import AddLink from './AddLink.svelte';
</script>

<h1 class="text-2xl">Create New Share Link</h1>

<Tabs.Root value="all">
	<Tabs.Content value="all">
		<Card.Root>
			<Card.Header>
				<Card.Description>Setup your Links.</Card.Description>
			</Card.Header>
			<Card.Content>
				<AddLink
					data={data.form}
					myApps={data.respApps.apps}
					networks={data.respNets.custom_networks}
					myDomains={data.respDomains.links}
				/>
			</Card.Content>
			<Card.Footer></Card.Footer>
		</Card.Root>
	</Tabs.Content>
</Tabs.Root>
