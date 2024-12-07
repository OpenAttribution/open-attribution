<script lang="ts">
	let { data } = $props();
	let title = 'Documentation | How to use OpenAttribution to track your ads';
	const description =
		'Documentation for OpenAttribution. Learn how to track your ads and analyze your ad data on your own servers. Get the features of a full MMP without the vendor lock-in or data scraping.';
	const keywords =
		'documenation, docs, open source, openattribution, open attribution, mmp, mobile, ad tracking, ad analysis, ad platform';
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
	srcdoc={data.props.mydocs}
	class="h-screen w-full"
	frameborder="0"
	title="Docs Content"
	id="frame"
	style="color-scheme: dark;"
></iframe>
