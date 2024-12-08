<script lang="ts">
	import { page } from '$app/stores';
	let { data } = $props();
</script>

{#await data.appData}
	loading ...
{:then app}
	{console.log(app)}
	<h1>App: {app.app.name}</h1>
	<h1>StoreId: {app.app.store_id}</h1>
	<h1>Store: {app.app.store}</h1>
	<h1>Created: {app.app.created_at}</h1>
	<h2 class="h2">App: {$page.params.storeid}</h2>
{:catch}
	<h1>App: Not Found</h1>
	}
{/await}
