<script lang="ts">
	let { data } = $props();
</script>

<iframe
	srcdoc={data.props.myblog}
	class="w-full h-screen"
	frameborder="0"
	title="Blog Content"
	id="frame"
	style="color-scheme: dark;"
></iframe>
