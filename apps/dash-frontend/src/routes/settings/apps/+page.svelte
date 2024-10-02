<script lang="ts">
	import { Button } from '$lib/components/ui/button/index';
	import * as Card from '$lib/components/ui/card/index';
	import { Checkbox } from '$lib/components/ui/checkbox/index';
	import { Input } from '$lib/components/ui/input/index';
	import * as Table from '$lib/components/ui/table';
	import * as Tabs from '$lib/components/ui/tabs';
	import { CirclePlus, Trash2 } from 'lucide-svelte';

	import type { PageData } from '../$types';

	import { CheckCircle, XCircle, AlertCircle } from 'lucide-svelte';

	const { data } = $props<{ data: PageData }>();

	let showForm = $state(false);

	function toggleForm() {
		showForm = !showForm;
	}

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

<h1 class="text-2xl">App Settings</h1>
<Tabs.Root value="all">
	<Tabs.Content value="all">
		<Card.Root>
			<Card.Header>
				<Card.Title>
					<div class="flex items-center">Apps</div>
				</Card.Title>
				<Card.Description>Manage your Apps and their settings.</Card.Description>
			</Card.Header>
			<Card.Content>
				<div class="flex items-center gap-2">
					<Button on:click={toggleForm} size="sm" class="h-8 gap-1">
						<CirclePlus class="h-3.5 w-3.5" />
						<span class="sr-only sm:not-sr-only sm:whitespace-nowrap">New App (pop)</span>
					</Button>
					{#if showForm}
						<div class="modal">
							<form method="POST" action="?/createApp">
								<label>
									Store ID
									<input name="store_id" type="text" />
								</label>
								<label>
									Name
									<input name="app_name" type="text" />
								</label>
								<label>
									Store
									<input name="store" type="number" />
								</label>
								<button type="submit">-> Save</button>
							</form>
						</div>
					{/if}
				</div>

				{#await data.respData}
					Loading...
				{:then mydata}
					<Table.Root>
						<Table.Header>
							<Table.Row>
								<Table.Head>App</Table.Head>
								<Table.Head></Table.Head>
								<Table.Head>Status</Table.Head>
							</Table.Row>
						</Table.Header>
						<Table.Body>
							{#if mydata.apps && mydata.apps.length > 0}
								{#each mydata.apps.slice(0, 10) as entry (entry.name)}
									<Table.Row>
										<Table.Cell>{entry.name}</Table.Cell>

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
