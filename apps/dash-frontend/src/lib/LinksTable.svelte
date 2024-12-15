<script lang="ts">
	import SettingsTable from '$lib/my-table/SettingsTable.svelte';

	let { tableData, isDomains } = $props();

	let columns = $state([{ accessorKey: '', header: '' }]);
	let actionDeleteString: string = $state('');

	const domainColumns = [
		{ accessorKey: 'domain_url', header: 'Domain' },
		{ accessorKey: 'created_at', header: 'Created At' },
		{ accessorKey: 'db_id', header: 'Delete' }
	];

	const linkColumns = [
		{ accessorKey: 'full_url', header: 'URL' },
		{
			accessorKey: 'network_name',
			header: 'Network'
		},
		{ accessorKey: 'google_app_name', header: 'Google Play Store App' },
		{ accessorKey: 'apple_app_name', header: 'Apple Store App' },
		{ accessorKey: 'web_landing_page', header: 'Web Landing Page' },
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
		},
		{
			accessorKey: 'db_id',
			header: 'Delete'
		}
	];

	if (isDomains) {
		columns = domainColumns;
		actionDeleteString = '?/deleteClientDomain';
	} else {
		columns = linkColumns;
		actionDeleteString = '?/deleteLink';
	}
</script>

{#await tableData}
	Loading...
{:then tableData}
	<SettingsTable {columns} data={tableData} {actionDeleteString} />
{/await}
