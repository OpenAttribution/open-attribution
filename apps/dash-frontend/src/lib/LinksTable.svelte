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
		{ accessorKey: 'google_store_app', header: 'Google Play Store App' },
		{ accessorKey: 'apple_store_app', header: 'Apple Store App' },

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
