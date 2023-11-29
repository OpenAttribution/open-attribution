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
<div class="grid grid-cols-2 gap-4 lg:gap-16 p-4 lg:p-48">
	<div class="card p-4">
		<div class="card-header"><h2 class="h3">Full Ownership & Privacy</h2></div>
		<div class="card-footer">
			<p>Self-hosted means that your data isn't being mined for value by other companies.</p>
		</div>
	</div>

	<div class="card p-4">
		<div class="card-header"><h2 class="h3">Data Pipeline & Storage</h2></div>
		<div class="card-footer">
			<p>
				Data processing pipelines efficiently store raw data and aggregate for fast dash queries.
			</p>
			<p>Analytics</p>
		</div>
	</div>

	<div class="card p-4">
		<div class="card-header"><h2 class="h3">Attribution Models</h2></div>
		<div class="card-footer">
			<p>
				You control your attribution models. Last click too old? Try new multi-touch models or
				modern CTV models.
			</p>
		</div>
	</div>

	<div class="card p-4">
		<div class="card-header"><h2 class="h3">Full MMP Analytics Dashboard</h2></div>
		<div class="card-footer">
			<p>
				A full MMP dashboard for your team. User permissions, apps, network settings and ad campaign
				analytics.
			</p>
		</div>
	</div>
</div>
