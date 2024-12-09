<script lang="ts">
	import SettingsTable from '$lib/my-table/SettingsTable.svelte';
	import { Trash2 } from 'lucide-svelte';

	let { tableData, isDomains } = $props();

	const domainColumns = [
		{ accessorKey: 'domain_url', header: 'Domain' },
		{ accessorKey: 'created_at', header: 'Created At' },
		{ accessorKey: 'db_id', header: 'Delete' }
	];

	const linkColumns = [
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
		},
		{
			accessorKey: 'db_id',
			header: 'Delete'
		}
	];

	const columns = isDomains ? domainColumns : linkColumns;
</script>

{#await tableData}
	Loading...
{:then tableData}
	<SettingsTable {columns} data={tableData} includeDelete={true} />
{/await}
