<script lang="ts">
	let { data } = $props();

	let title = 'Blog | OpenAttribution Latest News';
	const description =
		'Latest news and updates from the OpenAttribution team. Learn about the latest features, updates, and improvements.';
	const keywords =
		'blog, openattribution, open source, mmp, mobile, ad tracking, ad analysis, ad platform';
</script>

<svelte:head>
	<title>{title}</title>
	<meta property="og:title" content={title} />
	<meta name="twitter:title" content={title} />
	<meta name="description" content={description} />
	<meta name="keywords" content={keywords} />
	<meta property="og:description" content={description} />
	<meta name="twitter:description" content={description} />
</svelte:head>

<iframe
	srcdoc={data.props.myblog}
	class="h-screen w-full"
	frameborder="0"
	title="Blog Content"
	id="frame"
	style="color-scheme: dark;"
></iframe>
