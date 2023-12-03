<script lang="ts">
	import { embedDashboard } from "@superset-ui/embedded-sdk";
	import { onMount } from 'svelte';

	export let data;

	let myProps  = data.props.data
	let myToken: Promise<string> = myProps.token
	console.info(`GUEST TOKEN: ${myToken}`)

	onMount(() => {
		embedDashboard({
  			id: "d7012462-5f39-48f1-96b4-fee1d7b2b3ac", // given by the Superset embedding UI
  			supersetDomain: "http://localhost:8088",
  			mountPoint: document.getElementById("my-superset-container"), // any html element that can contain an iframe
  			fetchGuestToken: () => myToken,
  			dashboardUiConfig: { // dashboard UI config: hideTitle, hideTab, hideChartControls, filters.visible, filters.expanded (optional)
      			// hideTitle: true,
      			filters: {
          			 expanded: true,
      			}
  			},
			});
	})
</script>

<h1 class='h1'>hi</h1>

<div id="my-superset-container"></div>

<div>
<!-- <iframe id="my-superset-container2" src="http://localhost:8088/superset/dashboard/5/?standalone=true"></iframe> -->
</div>

