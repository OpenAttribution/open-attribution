<script lang="ts">
	import OverviewTable from '$lib/my-table/OverviewTable.svelte';

	let { tableData } = $props();

	const columns = [
		{
			accessorKey: 'share_slug',
			header: 'URL Slug'
		},
		{
			accessorKey: 'network_name',
			header: 'Network'
		},
		{
			accessorKey: 'campaign_name',
			header: 'Campaign Name'
		},
		{
			accessorKey: 'ad_name',
			header: 'Ad Name'
		},
		{
			accessorKey: 'created_at',
			header: 'Created At'
		}
	];
</script>

{#await tableData}
	Loading...
{:then tableData}
	<OverviewTable {columns} data={tableData} />
{/await}
