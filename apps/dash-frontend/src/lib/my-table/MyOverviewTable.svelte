<script lang="ts" generics="TData, TValue">
	import {
		type ColumnDef,
		type PaginationState,
		getCoreRowModel,
		getPaginationRowModel
	} from '@tanstack/table-core';

	import { createSvelteTable, FlexRender } from '$lib/components/ui/data-table/index.js';
	import * as Table from '$lib/components/ui/table/index.js';

	type DataTableProps<TData, TValue> = {
		data: TData[];
		columns: ColumnDef<TData, TValue>[];
	};

	let { data, columns }: DataTableProps<TData, TValue> = $props();

	// this is confirming the columns are being passed in correctly
	console.log('Data table columns', columns[0].accessorKey, columns[1].accessorKey);

	let pagination = $state<PaginationState>({ pageIndex: 0, pageSize: 10 });

	const table = createSvelteTable({
		get data() {
			return data;
		},
		columns,
		state: {
			get pagination() {
				return pagination;
			}
		},
		onPaginationChange: (updater) => {
			if (typeof updater === 'function') {
				pagination = updater(pagination);
			} else {
				pagination = updater;
			}
		},
		getCoreRowModel: getCoreRowModel(),
		getPaginationRowModel: getPaginationRowModel()
	});
</script>

<div class="rounded-md border">
	{columns[0].accessorKey}
	{columns[1].accessorKey}
	<Table.Root>
		<Table.Header>
			{#each table.getHeaderGroups() as headerGroup (headerGroup.id)}
				<Table.Row>
					{#each headerGroup.headers as header (header.id)}
						<Table.Head>
							{#if !header.isPlaceholder}
								<FlexRender
									content={header.column.columnDef.header}
									context={header.getContext()}
								/>
							{/if}
						</Table.Head>
					{/each}
				</Table.Row>
			{/each}
		</Table.Header>
		<Table.Body>
			{#each table.getRowModel().rows as row (row.id)}
				<Table.Row data-state={row.getIsSelected() && 'selected'}>
					{#each row.getVisibleCells() as cell (cell.id)}
						<Table.Cell>
							<FlexRender content={cell.column.columnDef.cell} context={cell.getContext()} />
						</Table.Cell>
					{/each}
				</Table.Row>
			{:else}
				<Table.Row>
					<Table.Cell colspan={columns.length} class="h-24 text-center">No results.</Table.Cell>
				</Table.Row>
			{/each}
		</Table.Body>
	</Table.Root>
</div>
