<script lang="ts">
	let h1title = 'Open Source MMP & Full Data Privacy';
	let h2title = "Control who sees your company's ad data.";

	let title = 'Product | OpenAttribution MMP';
	const description =
		'OpenAttribution is an open source mobile attribution platform (MMP) for tracking and analyzing ad campaigns.';
	const keywords =
		'openattribution, open attribution, mmp, mobile, ad tracking, ad analysis, ad platform';
	('about, history, openattribution, open source, mmp, mobile, ad tracking, ad analysis, ad platform');
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

<div class="mx-8 md:mx-16 lg:mx-32">
	<div
		class="card preset-filled-surface-100-900 my-12 flex items-center justify-center text-center lg:mt-8"
	>
		<div class="py-12">
			<h1 class="h1 text-center">{h1title}</h1>
			<h2 class="h2 text-primary-500 text-center">{h2title}</h2>
			<h4 class="h4 p-2 text-center lg:p-4">
				Fully hosted means your user data sits on your servers and is only seen by your teams.
			</h4>
		</div>
	</div>

	<div
		class="card preset-filled-surface-100-900 my-12 flex items-center justify-center text-center lg:mt-8"
	>
		<div class="py-12">
			<h2 class="h2 text-center">Own Your Data</h2>
			<h2 class="h2 text-primary-500 text-center">Control Your Ad Attribution</h2>
			<h4 class="h4 p-2 text-center lg:p-4">
				<p>
					Data processing pipelines efficiently store raw data and aggregate for fast dash queries.
				</p>
				<p>Use the built in analytics dashboard to see all the data you expect.</p>
				<p>
					Want to bring your own BI tool? No problem, since it's your data there are no proprietary
					restrictions for exporting or connecting other tools.
				</p>
			</h4>
			<div class=" flex items-center"></div>
		</div>
	</div>

	<div
		class="card preset-filled-surface-100-900 my-12 flex items-center justify-center text-center lg:mt-8"
	>
		<div class="py-12">
			<h2 class="h2 text-center">Attribution Models</h2>
			<h2 class="h2 text-primary-500 text-center">Full control over the attribution models</h2>
			<h4 class="h4 p-2 text-center lg:p-4">
				Control your attribution models. Last click too old? Try new multi-touch models or modern
				CTV models. Attribution models are not set in stone, you can flip between attribution models
				at any time to see how different measurement techniques weight different advertising
				campagins.
			</h4>
		</div>
	</div>
</div>
