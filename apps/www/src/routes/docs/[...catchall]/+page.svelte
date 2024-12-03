<script lang="ts">
	let { data } = $props();
</script>

<iframe
	srcdoc={data.props.mydocs}
	class="w-full h-screen"
	frameborder="0"
	title="Docs Content"
	id="frame"
	style="color-scheme: dark;"
></iframe>
