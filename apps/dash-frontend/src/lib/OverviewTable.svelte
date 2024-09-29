<script lang="ts">
	import * as Table from '$lib/components/ui/table/index.js';

	import type { OverviewEntries } from '../types';

	let { overviewData = [] as OverviewEntries } = $props();
</script>

<Table.Root>
	<Table.Header>
		<Table.Row>
			<Table.Head>Store ID</Table.Head>
			<Table.Head>Network</Table.Head>
			<Table.Head>Campaign</Table.Head>
			<Table.Head class="text-right">Impressions</Table.Head>
			<Table.Head class="text-right">Clicks</Table.Head>
			<Table.Head class="text-right">Installs</Table.Head>
			<Table.Head class="text-right">Revenue</Table.Head>
		</Table.Row>
	</Table.Header>
	<Table.Body>
		{#if overviewData && overviewData.length > 0}
			{#each overviewData.slice(0, 10) as entry (entry.store_id + entry.network + entry.campaign_name)}
				<Table.Row>
					<Table.Cell>{entry.store_id}</Table.Cell>
					<Table.Cell>{entry.network}</Table.Cell>
					<Table.Cell>{entry.campaign_name}</Table.Cell>
					<Table.Cell class="text-right">{entry.impressions}</Table.Cell>
					<Table.Cell class="text-right">{entry.clicks}</Table.Cell>
					<Table.Cell class="text-right">{entry.installs}</Table.Cell>
					<Table.Cell class="text-right">{parseFloat(entry.revenue).toFixed(4)}</Table.Cell>
				</Table.Row>
			{/each}
		{/if}
	</Table.Body>
</Table.Root>
