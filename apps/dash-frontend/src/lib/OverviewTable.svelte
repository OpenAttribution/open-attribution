<script lang="ts">
	import * as Table from '$lib/components/ui/table/index.js';

	import type { GroupedEntry } from '../types';

	import { tableDimensions } from '$lib/constants';


	let {
		overviewData = [] as GroupedEntry[],
		dimensionA,
		dimensionB
	} = $props();

</script>

<Table.Root>
	<Table.Header>
		<Table.Row>
			<Table.Head>{tableDimensions.find(dim => dim.value === dimensionA)?.label || dimensionA}</Table.Head>
			<Table.Head>{tableDimensions.find(dim => dim.value === dimensionB)?.label || dimensionB}</Table.Head>
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
					<Table.Cell class="text-right">{entry.impressions}</Table.Cell>
					<Table.Cell class="text-right">{entry.clicks}</Table.Cell>
					<Table.Cell class="text-right">{entry.installs}</Table.Cell>
					<Table.Cell class="text-right">{entry.revenue.toFixed(4)}</Table.Cell>
				</Table.Row>
			{/each}
		{/if}
	</Table.Body>
</Table.Root>
