<script lang="ts">
	export let data;
	import { page } from '$app/stores';

	// Reactive statement to process $page.url.pathname
	$: processedPathname = $page.url.pathname.startsWith('/docs/')
		? $page.url.pathname.replace('/docs/', '') // Removes '/docs/' from the pathname
		: $page.url.pathname;
</script>

<div class="border-b border-gray-200"></div>

<h2 class="h2">{processedPathname}</h2>

<!-- THIS DOESN"T WORK: BAD HTML/HEADERS -->
<!-- srcdoc={data.props.mydocs} -->
<!-- {@html data.props.mydocs} -->

<!-- without base in header USING /documentation/ doesn't work since then children pages load as documentation which is the static site?  -->
<!-- with base in header USING /documentation/ doesn't work since then children pages load content but fail to load assets from /documentation instead from /documentation/child/ (no dir there)  -->

<iframe
	class="w-full h-full"
	src={`/docs/${processedPathname}index.html`}
	frameborder="0"
	title="Docs Content"
	id="frame"
	style="color-scheme: dark;"
/>
