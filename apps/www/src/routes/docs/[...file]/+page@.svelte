<script lang="ts">
	export let data;
</script>

<div class="border-b border-gray-200"></div>

<iframe
	srcdoc={data.props.myhtml}
	class="bg-[#ececec] w-full h-full"
	frameborder="0"
	title="Project"
	id="frame"
	style="color-scheme: dark;"
/>
