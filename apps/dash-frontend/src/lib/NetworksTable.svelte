<script lang="ts">
	import * as Table from '$lib/components/ui/table/index.js';

	import type { NetworkEntries } from '../types';

	let { overviewData = [] as NetworkEntries } = $props();
</script>

<Table.Root>
	<Table.Header>
		<Table.Row>
			<Table.Head>Network</Table.Head>
		</Table.Row>
	</Table.Header>
	<Table.Body>
		{#if overviewData && overviewData.length > 0}
			{#each overviewData.slice(0, 10) as entry (entry.name)}
				<Table.Row>
					<Table.Cell>{entry.name}</Table.Cell>
				</Table.Row>
			{/each}
		{/if}
	</Table.Body>
</Table.Root>
