<script type="ts">
	import { goto } from '$app/navigation';
	function redirectToProduct() {
		goto('/product');
	}
	function redirectToDocs() {
		// goto('/docs');
		window.location.href = '/docs/index.html';
	}
</script>

<div class="p-2">
	<div class="card mx-8 lg:mx-96 my-12 lg:my-24 flex items-center justify-center text-center">
		<div class="py-12">
			<h1 class="h1 text-center">Own Your Data</h1>
			<h1 class="h1 text-center text-secondary-500">Control Your Ad Attribution</h1>
			<h4 class="h4 text-center p-2 lg:p-4">
				Open Attribution is an open source MMP alternative. Fully host and own your data by
				overseeing it's storage, manage your data pipeline and control your advertising campaign
				attribution rules.
			</h4>

			<div class="flex justify-center gap-2">
				<button
					type="button"
					class="btn variant-outline-secondary mr-4 justify-center"
					on:click={redirectToProduct}>Learn More</button
				>
				<button type="button" class="btn variant-outline-primary" on:click={redirectToDocs}
					>Documentation</button
				>
			</div>
		</div>
	</div>
</div>
<div class="p-4" />
<div class="card p-4">Basic</div>
