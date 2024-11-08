<script lang="ts">
	import { TableHandler, Datatable, ThSort, ThFilter } from '@vincjo/datatables'
	import type { GroupedEntry } from '../types';
	import { tableDimensions } from '$lib/constants';

	let {
		overviewData = [] as GroupedEntry[],
		dimensionA,
		dimensionB
	} = $props();

	const table = new TableHandler(overviewData, { rowsPerPage: 10 })

</script>

<!-- <h1 class='h1 text-center text-xl'>Overview Table {dimensionA} {dimensionB}: {overviewData.length}</h1> -->

<!-- basic here provides pagination and search -->
<Datatable basic {table}>
    <table>
        <thead>
			<tr>
				<ThSort {table} field={dimensionA}>{tableDimensions.find(dim => dim.value === dimensionA)?.label || dimensionA}></ThSort>
				<ThSort {table} field={dimensionB}>{tableDimensions.find(dim => dim.value === dimensionB)?.label || dimensionB}</ThSort>
				<ThSort {table} field="impressions">Impressions</ThSort>
				<ThSort {table} field="clicks">Clicks</ThSort>
				<ThSort {table} field="installs">Installs</ThSort>
				<ThSort {table} field="revenue">Revenue</ThSort>
			</tr>
			<tr>
				<ThFilter {table} field={dimensionA}>{tableDimensions.find(dim => dim.value === dimensionA)?.label || dimensionA}></ThFilter>
				<ThFilter {table} field={dimensionB}>{tableDimensions.find(dim => dim.value === dimensionB)?.label || dimensionB}></ThFilter>
			</tr>
        </thead>
        <tbody>
            {#each table.rows as row}
                <tr>
					<td>{row[dimensionA as keyof typeof row]}</td>
					<td>{row[dimensionB as keyof typeof row]}</td>
					<td class="text-right">{row.impressions}</td>
					<td class="text-right">{row.clicks}</td>
					<td class="text-right">{row.installs}</td>
					<td class="text-right">{row.revenue.toFixed(4)}</td>
                    <td>{row.first_name}</td>
                    <td>{row.last_name}</td>
                    <td>{row.email}</td>
                </tr>
            {/each}
        </tbody>
    </table>
</Datatable>

<div class= 'p-8'></div>

<style>
    table {
        border: 1px solid var(--grey);
        border-radius: 8px;
        margin: 16px 0 0 0;
    }
    
    thead :global(th:last-child) {
        border-radius: 0 8px 0 0;
    }
    td :global(svg) {
        margin-right: 6px;
    }
    
    tbody td {
        border: none !important;
        border-bottom: 1px solid var(--grey-lighten) !important;
        padding: 10px 20px !important;
    }
    tr:last-child td{
        border: none !important;
    }
    tbody tr:last-child td:first-child{
        border-radius: 0 0 0 8px;
    }
    tbody tr:last-child td:last-child{
        border-radius: 0 0 8px 0;
    }
    

    tbody tr:hover {
        background-color: rgb(33, 30, 34) !important;
    }


</style>