<script lang="ts">
	import OverviewTable from '$lib/my-table/OverviewTable.svelte';

	let { appLinks } = $props();

	const columns = [
		{
			accessorKey: 'network',
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
			accessorKey: 'ad_id',
			header: 'Ad ID'
		},
		{
			accessorKey: 'created_at',
			header: 'Created At'
		}
	];
</script>

{#await appLinks}
	Loading...
{:then appLinks}
	<OverviewTable {columns} data={appLinks} />
{/await}
