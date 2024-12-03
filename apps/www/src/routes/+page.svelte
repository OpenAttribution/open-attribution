<script lang="ts">
	import { goto } from '$app/navigation';
	function redirectToProduct() {
		goto('/product');
	}
	function redirectToDocs() {
		window.location.href = '/docs';
	}
</script>

<div class="card preset-outlined-primary-500 p-4 mx-16 lg:mx-32 mt-8 text-center">
	<h3 class="h3 text-primary-500">🏗️ Early Alpha: Under Construction 🏗️</h3>
	<p class="">
		This open source project is under construction in the very early alpha stages and is not yet
		ready. If you're interested in helping out please contact or reach out on <a
			href="https://github.com/OpenAttribution/open-attribution"
			target="_blank"
			rel="noreferrer">GitHub</a
		>
		or <a href="https://discord.gg/Z5ueYE3Ct3" target="_blank" rel="noreferrer">Discord</a>.
	</p>
</div>

<div
	class="card preset-filled-surface-100-900 mx-8 md:mx-16 lg:mx-32 my-12 lg:mt-8 flex items-center justify-center text-center"
>
	<div class="py-12">
		<h1 class="h1 text-center">Own Your Data</h1>
		<h2 class="h2 text-center text-primary-500">Control Your Ad Attribution</h2>
		<h4 class="h4 text-center p-2 lg:p-4">
			Open Attribution is an open source MMP. Fully host your data by overseeing it's storage,
			manage your data pipeline and control your advertising campaign attribution rules.
		</h4>

		<div class="flex justify-center gap-2">
			<button
				type="button"
				class="btn preset-outlined-primary-500 mr-4 justify-center"
				onclick={redirectToProduct}>Learn More</button
			>
			<button type="button" class="btn preset-outlined-tertiary-500" onclick={redirectToDocs}
				>Documentation</button
			>
		</div>
	</div>
</div>

<div class="grid grid-cols-2 gap-4 lg:gap-16 p-4 lg:px-48">
	<div class="card preset-filled-surface-100-900 p-4">
		<div class="card-header"><h3 class="h3 text-primary-900-100">Full Ownership & Privacy</h3></div>
		<div class="card-footer">
			<p>Self-hosted means that your data isn't being mined for value by other companies.</p>
		</div>
	</div>

	<div class="card preset-filled-surface-100-900 p-4">
		<div class="card-header"><h3 class="h3 text-primary-900-100">Data Pipeline & Storage</h3></div>
		<div class="card-footer">
			<p>
				Data processing pipelines efficiently store raw data and aggregate for fast dash queries.
			</p>
			<p>Analytics</p>
		</div>
	</div>

	<div class="card preset-filled-surface-100-900 p-4">
		<div class="card-header"><h3 class="h3 text-primary-900-100">Attribution Models</h3></div>
		<div class="card-footer">
			<p>
				You control your attribution models. Last click too old? Try new multi-touch models or
				modern CTV models.
			</p>
		</div>
	</div>

	<div class="card preset-filled-surface-100-900 p-4">
		<div class="card-header">
			<h3 class="h3 text-primary-900-100">Full MMP Analytics Dashboard</h3>
		</div>
		<div class="card-footer">
			<p>
				A full MMP dashboard for your team. User permissions, apps, network settings and ad campaign
				analytics.
			</p>
		</div>
	</div>
</div>
