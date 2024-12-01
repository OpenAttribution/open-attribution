<script lang="ts">
	let { data } = $props();
</script>

<div class="border-b border-gray-200"></div>

<iframe
	srcdoc={data.props.mydocs}
	class="w-full h-full"
	frameborder="0"
	title="Docs Content"
	id="frame"
	style="color-scheme: dark;"
></iframe>
