<script lang="ts" generics="TData, TValue">
	import { Trash2 } from 'lucide-svelte';

	import {
		type ColumnDef,
		type PaginationState,
		type ColumnFiltersState,
		type VisibilityState,
		getCoreRowModel,
		getPaginationRowModel
	} from '@tanstack/table-core';

	import DataTablePagination from './pagination.svelte';

	import { Button } from '$lib/components/ui/button/index.js';
	import * as DropdownMenu from '$lib/components/ui/dropdown-menu/index.js';

	import { createSvelteTable, FlexRender } from '$lib/components/ui/data-table/index.js';
	import * as Table from '$lib/components/ui/table/index.js';

	type DataTableProps<TData, TValue> = {
		columns: ColumnDef<TData, TValue>[];
		data: TData[];
		includeDelete?: boolean;
	};

	let { data, columns, includeDelete = false }: DataTableProps<TData, TValue> = $props();

	// this is confirming the columns are being passed in correctly
	// console.log('Data table columns', columns[0].accessorKey, columns[1].accessorKey);

	let pagination = $state<PaginationState>({ pageIndex: 0, pageSize: 10 });

	let columnFilters = $state<ColumnFiltersState>([]);
	let columnVisibility = $state<VisibilityState>({});

	const table = createSvelteTable({
		get data() {
			return data;
		},
		get columns() {
			return columns;
		},
		state: {
			get pagination() {
				return pagination;
			},
			get columnFilters() {
				return columnFilters;
			},
			get columnVisibility() {
				return columnVisibility;
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
		getPaginationRowModel: getPaginationRowModel(),
		onColumnFiltersChange: (updater) => {
			if (typeof updater === 'function') {
				columnFilters = updater(columnFilters);
			} else {
				columnFilters = updater;
			}
		},
		onColumnVisibilityChange: (updater) => {
			if (typeof updater === 'function') {
				columnVisibility = updater(columnVisibility);
			} else {
				columnVisibility = updater;
			}
		}
	});
</script>

<div class="flex items-center py-4">
	<DropdownMenu.Root>
		<DropdownMenu.Trigger>
			{#snippet child({ props })}
				<Button {...props} variant="outline" class="ml-auto">Columns</Button>
			{/snippet}
		</DropdownMenu.Trigger>
		<DropdownMenu.Content align="end">
			{#if table.getRowModel().rows.length > 0}
				{#each table.getAllColumns().filter((col) => col.getCanHide()) as column (column.id)}
					<DropdownMenu.CheckboxItem
						class="capitalize"
						controlledChecked
						checked={column.getIsVisible()}
						onCheckedChange={(value) => column.toggleVisibility(!!value)}
					>
						{column.id}
					</DropdownMenu.CheckboxItem>
				{/each}
			{/if}
		</DropdownMenu.Content>
	</DropdownMenu.Root>
</div>

<div class="rounded-md border">
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
					{#if includeDelete}
						<Table.Cell>
							<form method="POST" action="?/deleteClientDomain">
								<input type="hidden" name="id" value={row.id} />
								<label class="inline-flex items-center">
									<button
										type="submit"
										aria-label="Delete integration"
										class="text-gray-400 hover:text-red-700"
									>
										<Trash2 size={20} />
									</button>
								</label>
							</form>
						</Table.Cell>
					{/if}
				</Table.Row>
			{:else}
				<Table.Row>
					<Table.Cell colspan={columns.length} class="h-24 text-center">No results.</Table.Cell>
				</Table.Row>
			{/each}
		</Table.Body>
	</Table.Root>
</div>

<div class="flex items-center justify-end space-x-2 py-4">
	<DataTablePagination {table} />
</div>
