<script lang="ts">
	import { embedDashboard } from "@superset-ui/embedded-sdk";
	import { onMount } from 'svelte';

	export let data;

	let myProps  = data.props.data
	let myToken: Promise<string> = myProps.token
	console.info(`GUEST TOKEN: ${myToken}`)

	onMount(() => {
 		const myDiv = document.getElementById("my-superset-container") // any html element that can contain an iframe
		if (myDiv) {
			embedDashboard({
  				id: "d7012462-5f39-48f1-96b4-fee1d7b2b3ac", // given by the Superset embedding UI
  				supersetDomain: "http://localhost:8088",
  				mountPoint: myDiv,
  				fetchGuestToken: () => myToken,
  				dashboardUiConfig: { // dashboard UI config: hideTitle, hideTab, hideChartControls, filters.visible, filters.expanded (optional)
      				// hideTitle: true,
      				filters: {
          				//  expanded: true,
      				}
  				},
				});
		}
		

	})
</script>

<h1 class='h1'>hi</h1>

<div class="h-screen">
<div id="my-superset-container" class="my-div-iframe h-screen w-full"/>
</div>

<style>
:global(.my-div-iframe iframe){
	height:100%;
	width:100%;
	border:4px solid red;
}	

</style>