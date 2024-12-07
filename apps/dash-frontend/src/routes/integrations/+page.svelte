<script lang="ts">
	import * as Card from '$lib/components/ui/card/index';
	import * as Table from '$lib/components/ui/table/index';
	import * as Tabs from '$lib/components/ui/tabs/index';

	import AddNetwork from '../../lib/AddCustomNetworkPopup.svelte';

	import { ListFilter, Trash2 } from 'lucide-svelte';
	import { Button } from '$lib/components/ui/button';
	import * as DropdownMenu from '$lib/components/ui/dropdown-menu';
	import { type PageData } from './$types';

	import { CheckCircle, XCircle, AlertCircle } from 'lucide-svelte';

	const { data } = $props<{ data: PageData }>();

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
</script>

<Tabs.Root value="all">
	<div class="flex items-center">
		<Tabs.List>
			<Tabs.Trigger value="all">All</Tabs.Trigger>
			<Tabs.Trigger value="active">Active</Tabs.Trigger>
			<Tabs.Trigger value="draft">Draft</Tabs.Trigger>
			<Tabs.Trigger value="archived" class="hidden sm:flex">Archived</Tabs.Trigger>
		</Tabs.List>
		<div class="ml-auto flex items-center gap-2">
			<DropdownMenu.Root>
				<DropdownMenu.Trigger>
					<Button variant="outline" size="sm" class="h-8 gap-1">
						<ListFilter class="h-3.5 w-3.5" />
						<span class="sr-only sm:not-sr-only sm:whitespace-nowrap"> Filter </span>
					</Button>
				</DropdownMenu.Trigger>
				<DropdownMenu.Content align="end">
					<DropdownMenu.Label>Filter by</DropdownMenu.Label>
					<DropdownMenu.Separator />
					<DropdownMenu.CheckboxItem checked>Active</DropdownMenu.CheckboxItem>
					<DropdownMenu.CheckboxItem>Draft</DropdownMenu.CheckboxItem>
					<DropdownMenu.CheckboxItem>Archived</DropdownMenu.CheckboxItem>
				</DropdownMenu.Content>
			</DropdownMenu.Root>

			<AddNetwork {data} />
		</div>
	</div>

	<Tabs.Content value="all">
		<Card.Root>
			<Card.Header>
				<Card.Title>Networks</Card.Title>
				<Card.Description>Manage your ad network integrations.</Card.Description>
			</Card.Header>
			<Card.Content>
				{#await data.respData}
					Loading...
				{:then mydata}
					<Table.Root>
						<Table.Header>
							<Table.Row>
								<Table.Head>Network</Table.Head>
								<Table.Head>Postback ID</Table.Head>
								<Table.Head>Status</Table.Head>
							</Table.Row>
						</Table.Header>
						<Table.Body>
							{#if mydata.networks && mydata.networks.length > 0}
								{#each mydata.networks.slice(0, 10) as entry (entry.name)}
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
				{/await}
			</Card.Content>
			<Card.Footer></Card.Footer>
		</Card.Root>
	</Tabs.Content>
</Tabs.Root>
