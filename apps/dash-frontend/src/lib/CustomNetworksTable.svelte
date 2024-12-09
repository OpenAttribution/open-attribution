<script lang="ts">
	import * as Table from '$lib/components/ui/table/index';

	import { CheckCircle, CircleDashed, AlertCircle, Trash2 } from 'lucide-svelte';

	let { tableData } = $props();

	// Helper function to get the appropriate icon and color for status
	const getStatusIcon = (status: String) => {
		switch (status) {
			case 'active':
				return { icon: CheckCircle, color: 'text-green-200' };
			case 'inactive':
				return { icon: CircleDashed, color: 'text-gray-500' };
			case 'error':
				return { icon: AlertCircle, color: 'text-red-500' };
			default:
				return { icon: AlertCircle, color: 'text-red-500' };
		}
	};
	console.log('MYDATA', tableData);
</script>

<Table.Root>
	<Table.Header>
		<Table.Row>
			<Table.Head>Network</Table.Head>
			<Table.Head>Postback ID</Table.Head>
			<Table.Head>Status</Table.Head>
		</Table.Row>
	</Table.Header>
	<Table.Body>
		{#if tableData && tableData.length > 0}
			{#each tableData.slice(0, 10) as entry (entry.name)}
				<Table.Row>
					<Table.Cell>{entry.name}</Table.Cell>
					<Table.Cell class="text-gray-400 italic mr-2">{entry.postback_id}</Table.Cell>
					<Table.Cell>
						{#if entry.is_custom}
							<form method="POST" action="?/deleteIntegration">
								<input type="hidden" name="id" value={entry.id} />
								<label class="flex items-center">
									<span class="text-gray-400 italic mr-2">(custom)</span>
									<button
										type="submit"
										aria-label="Delete integration"
										class="inline-flex items-center text-gray-400 hover:text-red-700"
									>
										<Trash2 size={20} />
									</button>
								</label>
							</form>
						{/if}
					</Table.Cell>

					<Table.Cell>
						{#if entry.status}
							{@const statusInfo = getStatusIcon(entry.status)}
							<statusInfo.icon class={statusInfo.color} size={20} />
						{/if}
					</Table.Cell>
				</Table.Row>
			{/each}
		{/if}
	</Table.Body>
</Table.Root>
