<script lang="ts">
	import '../app.css';
	import NavTabs from '$lib/NavTabs.svelte';
	import { AppBar } from '@skeletonlabs/skeleton-svelte';
	import githubIcon from '$lib/assets/github-mark-white.svg?raw';
	import discordIcon from '$lib/assets/discord-logo-white.svg?raw';
	interface Props {
		children?: import('svelte').Snippet;
	}

	let { children }: Props = $props();
</script>

<div class="grid h-screen grid-rows-[auto_1fr_auto]">
	<header class="sticky top-0 z-10">
		<AppBar
			leadBase="p-2 flex items-center"
			trailBase="p-2 flex items-center"
			centerBase="hidden md:flex items-center"
			padding="p-0"
		>
			{#snippet lead()}
				<a href="/" class="flex items-center">
					<strong class=" ml-4 text- xl md:text-2xl uppercase">Open Attribution</strong>
				</a>
			{/snippet}

			<div class="hidden lg:flex items-center justify-center">
				<NavTabs />
			</div>

			{#snippet trail()}
				<div class="inline">
					<a
						href="mailto:hello@openattribution.dev"
						class="btn preset-outlined-primary-900-100 p-4"
					>
						Email Contact
					</a>
					<a
						class="btn preset-outlined-tertiary-500 p-4"
						href="https://discord.gg/Z5ueYE3Ct3"
						target="_blank"
						rel="noreferrer"
					>
						{@html discordIcon}
					</a>
					<a
						class="btn preset-outlined-tertiary-500 p-4"
						href="https://github.com/OpenAttribution/open-attribution"
						target="_blank"
						rel="noreferrer"
					>
						{@html githubIcon}
						<h6 class="h6 justify-center text-center">GitHub</h6>
					</a>
				</div>
			{/snippet}
		</AppBar>
	</header>

	<main>
		{@render children?.()}
	</main>

	<!--  Mobile only footer -->
	<footer class="sticky bottom-0 z-10 bg-surface-50-950">
		<AppBar padding="p-0">
			<div class="inline-flex md:hidden p-2">
				<NavTabs />
			</div>
		</AppBar>
	</footer>
</div>
