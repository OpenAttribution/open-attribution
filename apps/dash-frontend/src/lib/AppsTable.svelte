<script lang="ts">
	import * as Table from '$lib/components/ui/table';
	import { CheckCircle, XCircle, AlertCircle, CirclePlus, Trash2 } from 'lucide-svelte';

	import IconAndroid from '$lib/svg/IconAndroid.svelte';
	import IconIOS from '$lib/svg/IconiOS.svelte';

	let { tableData } = $props();

	// Helper function to get the appropriate icon and color for status
	const getStatusIcon = (status: String) => {
		switch (status) {
			case 'active':
				return { icon: CheckCircle, color: 'text-green-200' };
			case 'inactive':
				return { icon: XCircle, color: 'text-gray-500' };
			case 'error':
				return { icon: AlertCircle, color: 'text-red-500' };
			default:
				return { icon: AlertCircle, color: 'text-red-500' };
		}
	};

	// Helper function to get the appropriate icon and color for status
	const getStoreIcon = (storeId: number) => {
		switch (storeId) {
			case 1:
				return { icon: IconAndroid, color: 'text-green-200' };
			case 2:
				return { icon: IconIOS, color: 'text-gray-500' };
			default:
				return { icon: AlertCircle, color: 'text-red-500' };
		}
	};
</script>

<Table.Root>
	<Table.Header>
		<Table.Row>
			<Table.Head>App</Table.Head>
			<Table.Head></Table.Head>
			<Table.Head>Store</Table.Head>
			<Table.Head>Store ID</Table.Head>
		</Table.Row>
	</Table.Header>
	<Table.Body>
		{#if tableData.apps && tableData.apps.length > 0}
			{#each tableData.apps.slice(0, 10) as entry ((entry.id, entry.store_id, entry.name))}
				<Table.Row>
					<a href="/settings/apps/{entry.store_id}">
						<Table.Cell>{entry.name}</Table.Cell>
					</a>
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
					<Table.Cell>
						{#if entry.store}
							{#if entry.store == 1}
								<IconAndroid size="40" />
							{:else if entry.store === 2}
								<IconIOS size="50" />
							{:else}
								MissingStoreIcon
							{/if}
						{/if}
					</Table.Cell>
					<Table.Cell>
						{#if entry.store_id}
							{entry.store_id}
						{/if}
					</Table.Cell>
				</Table.Row>
			{/each}
		{/if}
	</Table.Body>
</Table.Root>
