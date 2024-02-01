<script lang="ts">
	import discordIcon from '$lib/assets/discord-logo-white.svg?raw';
</script>

<div class="mx-8 mt-8">
	<h1 class="h1">About Open Attribution</h1>

	<aside class="alert variant-filled-secondary p-4 mx-8 lg:mx-96 mt-8">
		<div class="alert-message">
			<h3 class="h3">Mission Statement</h3>
			<p>
				Give app and game developers advertising tools that do not require 3rd party processing.
				Bring more data to the app developers by helping them to collect their impression and click
				data to leverage for better fraud detection, better data for AI tooling and business
				decisions.
			</p>
		</div>
	</aside>

	<div class="mx-8 lg:mx-32 mt-16">
		<h3 class="h3">Data Ownership</h3>
		<p>
			Own your company's advertising data without resorting to third party control. Our goal is to
			give developers control of their app advertising data rather than a third party. True
			ownership of your mobile app's data Paying someone else to hold and manage your app's data
			takes power away from app creators. Open Attribution is a suite of open source tools so that
			you can manage your advertising data ownership.
		</p>
		<br />

		<h3 class="h3">Open source community</h3>
		<p>
			Open Attribution is committed to building a community of developers who work together to build
			a secure ecosystem. Ready? This project is just starting, so if you're interested in using it
			please reach out before putting it into production. To learn more head to Getting Started to
			learn more.
		</p>

		<br />
		<h3 class="h3">Why do apps NEED attribution?</h3>
		<p>
			If you want to buy in-app advertisements, attribution a technical
			<strong>requirement</strong>, not a business option. Apps cannot use regular HTTP Urls to
			connect users, deep links are too limited. Historically MMPs stepped in to help solve this
			complex problem but by doing so became the arbiters of large amounts of data that some apps
			may wish to maintain control over. Read more about the historical background here.
		</p>
		<br />

		<h3 class="h3">Want to get in touch?</h3>
		<a
			class="btn btn-sm variant-ghost-surface"
			href="https://discord.gg/Z5ueYE3Ct"
			target="_blank"
			rel="noreferrer"
		>
			<div class="inline-flex items-center">
				{@html discordIcon}
			</div>
		</a>
		<br />
		<a href="mailto:hello@openattribution.dev">
			<button type="button" class="btn variant-outline-secondary mr-4 justify-center"
				>Contact</button
			>
		</a>
	</div>
	<br />
</div>
