<script lang="ts">
	import * as Table from '$lib/components/ui/table/index.js';

	import type { OverviewEntries } from '../types';

	let { overviewData = [] as OverviewEntries } = $props();
</script>

<Table.Root>
	<Table.Header>
		<Table.Row>
			<Table.Head>Network</Table.Head>
		</Table.Row>
	</Table.Header>
	<Table.Body>
		{#if overviewData && overviewData.length > 0}
			{#each overviewData.slice(0, 10) as entry (entry.network)}
				<Table.Row>
					<Table.Cell>{entry.network}</Table.Cell>
				</Table.Row>
			{/each}
		{/if}
	</Table.Body>
</Table.Root>
