<script lang="ts">
	import { onMount } from 'svelte';

	import { PUBLIC_SUPERSET_BROWSER_HOST } from '$env/static/public';

	// NOTE: import { embedDashboard } should be the correct way, but throws Vite error?
	import { embedDashboard } from '@superset-ui/embedded-sdk';
	// import * as pkg from '@superset-ui/embedded-sdk';
	// console.log('mypkg', pkg);
	// const { embedDashboard } = pkg;

	export let data;

	if (data.props) {
		let myProps = data.props.data;
		let myToken: Promise<string> = myProps.token;
		console.info(`GOT GUEST TOKEN`);

		onMount(() => {
			const myDiv = document.getElementById('my-superset-container');
			if (myDiv) {
				embedDashboard({
					id: data.dashboardID,
					supersetDomain: PUBLIC_SUPERSET_BROWSER_HOST,
					mountPoint: myDiv,
					fetchGuestToken: () => myToken,
					dashboardUiConfig: {
						// dashboard UI config: hideTitle, hideTab, hideChartControls, filters.visible, filters.expanded (optional)
						hideTitle: true,
						filters: {
							expanded: true
						}
					}
				});
			}
		});
	} else {
		console.log('Embedded superset dashboard failed to load');
	}
</script>

<h1 class="h1">Open-Attribution Demo</h1>
<h1 class="h6">Please reach out if you have questions.</h1>

<div class="h-screen">
	<div id="my-superset-container" class="my-div-iframe h-screen w-full" />
</div>

<style>
	:global(.my-div-iframe iframe) {
		height: 100%;
		width: 100%;
	}
</style>
