<script lang="ts">
	let h1title = 'Simple, Transparent Pricing';
	let h2title = "Choose the plan that's right for your business";
	let title = 'Pricing | OpenAttribution MMP';
	const description =
		'OpenAttribution pricing plans - from free self-hosted to enterprise solutions.';
	const keywords = 'openattribution, pricing, free, self-hosted, mmp, mobile attribution platform';
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

<div class="mx-8 md:mx-16 lg:mx-96">
	<div
		class="card preset-filled-surface-100-900 my-12 flex items-center justify-center text-center lg:mt-8"
	>
		<div class="py-12">
			<h1 class="h1 text-center">{h1title}</h1>
			<h2 class="h2 text-primary-500 text-center">{h2title}</h2>
			<h4 class="h4 p-2 text-center lg:p-4">
				Choose between our free self-hosted option or our upcoming hosted solutions designed to
				scale with your needs.
			</h4>
		</div>
	</div>

	<div class="my-12 grid grid-cols-1 gap-6 md:grid-cols-4">
		<!-- Self-Hosted Tier -->
		<div class="card preset-filled-surface-100-900 flex h-full flex-col p-6">
			<div class="flex items-start justify-between">
				<div>
					<h3 class="h3 mb-0">Alpha</h3>
					<p class="text-primary-500 font-bold">Self-Hosted</p>
				</div>
				<span class="badge variant-filled-primary">Open Source</span>
			</div>
			<div class="py-8">
				<p class="h2 font-bold">Free</p>
				<p class="opacity-75">Forever</p>
			</div>
			<div class="flex-1">
				<ul class="space-y-4">
					<li class="flex items-start gap-2">
						<div class="text-primary-500">✓</div>
						<span>Full data ownership & privacy</span>
					</li>
					<li class="flex items-start gap-2">
						<div class="text-primary-500">✓</div>
						<span>Raw data access</span>
					</li>
					<li class="flex items-start gap-2">
						<div class="text-primary-500">✓</div>
						<span>Community support</span>
					</li>
				</ul>
			</div>
			<div class="pt-8">
				<a class="btn preset-outlined-primary-500 w-full" href="/docs/getting_started/installation/"
					><p>Alpha in Development</p></a
				>
			</div>
		</div>
		<!-- Basic Hosted Tiers (Coming Soon) -->
		<div class="card preset-filled-surface-100-900 flex h-full flex-col p-6 opacity-50">
			<div class="flex items-start justify-between">
				<div>
					<h3 class="h3 mb-0">Indie</h3>
					<p class="text-primary-500 font-bold">Hosted</p>
				</div>
				<span class="badge variant-ghost">Coming Soon</span>
			</div>
			<div class="py-8">
				<p class="h2 font-bold">Free</p>
			</div>
			<div class="flex-1">
				<ul class="space-y-4">
					<li class="flex items-start gap-2">
						<div class="text-primary-500">✓</div>
						<span>Up to 1,000 monthly active users</span>
					</li>
					<li class="flex items-start gap-2">
						<div class="text-primary-500">✓</div>
						<span>Managed hosting & maintenance</span>
					</li>
					<li class="flex items-start gap-2">
						<div class="text-primary-500">✓</div>
						<span>All attribution models</span>
					</li>
					<li class="flex items-start gap-2">
						<div class="text-primary-500">✓</div>
						<span>Automated backups</span>
					</li>
					<li class="flex items-start gap-2">
						<div class="text-primary-500">✓</div>
						<span>Email support</span>
					</li>
				</ul>
			</div>
		</div>
		<div class="card preset-filled-surface-100-900 flex h-full flex-col p-6 opacity-50">
			<div class="flex items-start justify-between">
				<div>
					<h3 class="h3 mb-0">Business</h3>
					<p class="text-primary-500 font-bold">Hosted</p>
				</div>
				<span class="badge variant-ghost">Coming Soon</span>
			</div>
			<div class="py-8">
				<p class="h2 font-bold">$0.01</p>
				<p class="opacity-75">per monthly active user</p>
			</div>
			<div class="flex-1">
				<ul class="space-y-4">
					<li class="flex items-start gap-2">
						<div class="text-primary-500">✓</div>
						<span>Unlimited monthly active users</span>
					</li>
					<li class="flex items-start gap-2">
						<div class="text-primary-500">✓</div>
						<span>Managed hosting & maintenance</span>
					</li>
					<li class="flex items-start gap-2">
						<div class="text-primary-500">✓</div>
						<span>All attribution models</span>
					</li>
					<li class="flex items-start gap-2">
						<div class="text-primary-500">✓</div>
						<span>Automated backups</span>
					</li>
					<li class="flex items-start gap-2">
						<div class="text-primary-500">✓</div>
						<span>Email support</span>
					</li>
				</ul>
			</div>
			<div class="pt-8">
				<button class="btn variant-ghost-primary w-full" disabled>Contact for more Info</button>
			</div>
		</div>

		<!-- Enterprise Hosted Tier (Coming Soon) -->
		<div class="card preset-filled-surface-100-900 flex h-full flex-col p-6 opacity-50">
			<div class="flex items-start justify-between">
				<div>
					<h3 class="h3 mb-0">Enterprise</h3>
					<p class="text-primary-500 font-bold">Hosted</p>
				</div>
				<span class="badge variant-ghost">Coming Soon</span>
			</div>
			<div class="py-8">
				<p class="h2 font-bold">Custom</p>
				<p class="opacity-75">Contact for more info</p>
			</div>
			<div class="flex-1">
				<ul class="space-y-4">
					<li class="flex items-start gap-2">
						<div class="text-primary-500">✓</div>
						<span>Custom support</span>
					</li>
					<li class="flex items-start gap-2">
						<div class="text-primary-500">✓</div>
						<span>Custom services</span>
					</li>
					<li class="flex items-start gap-2">
						<div class="text-primary-500">✓</div>
						<span>Priority support</span>
					</li>
				</ul>
			</div>
			<div class="pt-8">
				<button class="btn variant-ghost-primary w-full" disabled>Contact for more Info</button>
			</div>
		</div>
	</div>

	<!-- FAQ Section -->
	<div class="card preset-filled-surface-100-900 my-12">
		<div class="p-8">
			<h2 class="h2 mb-8 text-center">Frequently Asked Questions</h2>

			<div class="space-y-6">
				<div>
					<h4 class="h4 text-primary-500">
						Will the free self-hosted version always be available?
					</h4>
					<p class="mt-2">
						Yes! Our commitment to open source means the self-hosted version will always be free to
						use, modify, and distribute under our open source license.
					</p>
				</div>

				<div>
					<h4 class="h4 text-primary-500">When will the hosted options be available?</h4>
					<p class="mt-2">
						We're currently focused on making our self-hosted version as robust as possible. Hosted
						options are planned for the future as we gather community feedback and needs. The goal
						is a viable company that can support the platform and provide a great service to our
						users.
					</p>
				</div>

				<div>
					<h4 class="h4 text-primary-500">Can I contribute to OpenAttribution?</h4>
					<p class="mt-2">
						Absolutely! We welcome contributions from the community. Check out our <a
							href="https://github.com/OpenAttribution/open-attribution"
							class="anchor">GitHub</a
						>
						to get started. Or join our
						<a href="https://discord.gg/Z5ueYE3Ct3" class="anchor">Discord</a> to chat with us and get
						involved.
					</p>
				</div>

				<div>
					<h4 class="h4 text-primary-500">How does pricing work for the Business tier?</h4>
					<p class="mt-2">
						The pricing goals not yet set in stone, but we will strive for prices that are
						sustainable and competitive.
					</p>
				</div>
			</div>
		</div>
	</div>
</div>
