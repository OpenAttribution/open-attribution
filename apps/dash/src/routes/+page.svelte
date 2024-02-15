<script lang="ts">
	import { embedDashboard } from '@superset-ui/embedded-sdk';

	// import * as pkg from '@superset-ui/embedded-sdk';
	// console.log('mypkg', pkg);
	// const { embedDashboard } = pkg;

	import { onMount } from 'svelte';

	// import { PUBLIC_SUPERSET_HOST_NAME } from '$env/static/public';

	export let data;

	let myProps = data.props.data;
	let myToken: Promise<string> = myProps.token;
	console.info(`GUEST TOKEN: ${myToken}`);

	onMount(() => {
		const myDiv = document.getElementById('my-superset-container'); // any html element that can contain an iframe
		if (myDiv) {
			embedDashboard({
				id: '47d4d3a7-c2b0-46c5-80ad-dc7ee0e68ef9', // given by the Superset embedding UI
				// supersetDomain: `http://${PUBLIC_SUPERSET_HOST_NAME}:8088`,
				supersetDomain: `http://localhost:8088`,
				mountPoint: myDiv,
				fetchGuestToken: () => myToken,
				dashboardUiConfig: {
					// dashboard UI config: hideTitle, hideTab, hideChartControls, filters.visible, filters.expanded (optional)
					// hideTitle: true,
					filters: {
						//  expanded: true,
					}
				}
			});
		}
	});
</script>

<h1 class="h1">Open-Attribution</h1>

<div class="h-screen">
	<div id="my-superset-container" class="my-div-iframe h-screen w-full" />
</div>

<style>
	:global(.my-div-iframe iframe) {
		height: 100%;
		width: 100%;
		border: 4px solid black;
	}
</style>
