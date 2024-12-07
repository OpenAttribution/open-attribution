<script lang="ts">
	import discordIcon from '$lib/assets/discord-logo-white.svg?raw';

	let title = 'About Open Attribution';
	const description =
		"About OpenAttribution's mission, and why we want to provide an open source mobile attribution platform (MMP) for tracking and analyzing ad campaigns.";
	const keywords =
		'about, history, openattribution, open source, mmp, mobile, ad tracking, ad analysis, ad platform';
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
	<div class="card preset-outlined-primary-500 mx-16 mt-8 p-4 text-center lg:mx-32">
		<h3 class="h3 text-primary-500">Mission Statement</h3>
		<p>
			Give app and game developers advertising tools that do not require 3rd party processing. Bring
			more data to the app developers by helping them to collect their impression and click data to
			leverage for better fraud detection, better data for AI tooling and business decisions.
		</p>

		<h4 class="h4">Support the Project</h4>

		<div class="flex justify-center gap-2">
			<a
				href="https://github.com/OpenAttribution/open-attribution"
				target="_blank"
				rel="noreferrer"
			>
				<button type="button" class="btn preset-outlined-primary-500 mr-4 justify-center"
					>Star on Github</button
				>
			</a>
			<a href="https://discord.gg/Z5ueYE3Ct3" target="_blank" rel="noreferrer">
				<button type="button" class="btn preset-outlined-tertiary-500">Join Discord</button>
			</a>
		</div>
	</div>

	<div class="card preset-filled-surface-100-900 mt-16 p-4">
		<h3 class="h3 text-primary-900-100">Data Ownership</h3>
		<p>
			Own your company's advertising data without resorting to third party control. Our goal is to
			give developers control of their app advertising data rather than a third party. True
			ownership of your mobile app's data Paying someone else to hold and manage your app's data
			takes power away from app creators. Open Attribution is a suite of open source tools so that
			you can manage your advertising data ownership.
		</p>
	</div>

	<div class="card preset-filled-surface-100-900 mt-16 p-4">
		<h3 class="h3 text-primary-900-100">Open source community</h3>
		<p>
			Open Attribution is committed to building a community of developers who work together to build
			a secure ecosystem. Ready? This project is just starting, so if you're interested in using it
			please reach out before putting it into production. To learn more head to Getting Started to
			learn more.
		</p>
	</div>

	<div class="card preset-filled-surface-100-900 mt-16 p-4">
		<h3 class="h3 text-primary-900-100">Why do apps NEED attribution?</h3>
		<p>
			If you want to buy in-app advertisements, attribution a technical
			<strong>requirement</strong>, not a business option. Apps cannot use regular HTTP Urls to
			connect users, deep links are too limited. Historically MMPs stepped in to help solve this
			complex problem but by doing so became the arbiters of large amounts of data that some apps
			may wish to maintain control over. Read more about the historical background here.
		</p>
	</div>

	<div class="card preset-filled-surface-100-900 mt-16 p-4">
		<h3 class="h3 text-primary-900-100">Want to get in touch?</h3>
		Feel free to join our small but growing community on Discord or reach our directly via email.
		<div class="flex flex-col items-center gap-4 p-8 md:flex-row md:gap-8">
			<a
				class="btn preset-filled-tertiary-500"
				href="https://discord.gg/Z5ueYE3Ct3"
				target="_blank"
				rel="noreferrer"
			>
				<div class="inline-flex h-12 w-24 items-center">
					{@html discordIcon}
				</div>
			</a>
			<br />
			<a href="mailto:hello@openattribution.dev">
				<button type="button" class="btn preset-outlined-tertiary-500">Contact via Email</button>
			</a>
		</div>
	</div>
	<br />
</div>
