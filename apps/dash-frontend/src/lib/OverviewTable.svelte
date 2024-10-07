<script lang="ts">
	import * as Table from '$lib/components/ui/table/index.js';

	import type { GroupedEntry } from '../types';

	let {
		overviewData = [] as GroupedEntry[],
		dimensionA = 'network' as String,
		dimensionB = 'store_id' as String
	} = $props();

	console.log('OVERVIEW DATA ROWS: ', Object.keys(overviewData).length);
</script>

<Table.Root>
	<Table.Header>
		<Table.Row>
			<Table.Head>{dimensionA}</Table.Head>
			<Table.Head>{dimensionB}</Table.Head>
			<Table.Head class="text-right">Impressions</Table.Head>
			<Table.Head class="text-right">Clicks</Table.Head>
			<Table.Head class="text-right">Installs</Table.Head>
			<Table.Head class="text-right">Revenue</Table.Head>
		</Table.Row>
	</Table.Header>
	<Table.Body>
		{#if overviewData && Object.keys(overviewData).length > 0}
			{console.log('OVERVIEW DATA ROWS: AFTER IF ', Object.keys(overviewData).length)}
			{#each overviewData.slice(0, 10) as entry}
				<Table.Row>
					<Table.Cell>{entry[dimensionA as keyof typeof entry]}</Table.Cell>
					<Table.Cell>{entry[dimensionB as keyof typeof entry]}</Table.Cell>
					<Table.Cell class="text-right">{entry['impressions']}</Table.Cell>
					<Table.Cell class="text-right">{entry.clicks}</Table.Cell>
					<Table.Cell class="text-right">{entry.installs}</Table.Cell>
					<Table.Cell class="text-right">{entry.revenue.toFixed(4)}</Table.Cell>
				</Table.Row>
			{/each}
		{/if}
	</Table.Body>
</Table.Root>
