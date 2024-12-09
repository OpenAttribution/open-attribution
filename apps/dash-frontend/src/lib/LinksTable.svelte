<script lang="ts">
	import OverviewTable from '$lib/my-table/OverviewTable.svelte';

	let { tableData } = $props();

	const columns = [
		{ accessorKey: 'client_domain', header: 'Domain' },

		{
			accessorKey: 'share_slug',
			header: 'URL Slug'
		},
		{
			accessorKey: 'network_name',
			header: 'Network'
		},
		{ accessorKey: 'play_store_app', header: 'Play Store App' },
		{ accessorKey: 'ios_app', header: 'iOS App' },

		{
			accessorKey: 'campaign_name',
			header: 'Campaign Name'
		},
		{
			accessorKey: 'ad_name',
			header: 'Ad Name'
		},
		{
			accessorKey: 'updated_at',
			header: 'Updated At'
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
