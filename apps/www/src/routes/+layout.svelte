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

<header class="sticky top-0 z-10">
	<!-- TODO: why is this not working<!--  -->
	<!-- gridColumns="grid-cols-[1fr_0_1fr] md:grid-cols-[0.4fr_1fr_0.3fr]" -->
	<AppBar leadBase="p-2" trailBase="p-2" padding="p-0">
		{#snippet lead()}
			<strong class=" ml-4 text- xl md:text-2xl uppercase">Open Attribution</strong>
		{/snippet}

		<div class="hidden lg:inline-flex">
			<NavTabs />
		</div>

		{#snippet trail()}
			<a href="mailto:hello@openattribution.dev">
				<button type="button" class="btn variant-outline-secondary mr-4 justify-center"
					>Contact</button
				>
			</a>
			<a
				class="btn btn-sm variant-ghost-surface"
				href="https://discord.gg/Z5ueYE3Ct3"
				target="_blank"
				rel="noreferrer"
			>
				<div class="inline-flex items-center">
					{@html discordIcon}
				</div>
			</a>
			<a
				class="btn btn-sm variant-ghost-surface"
				href="https://github.com/OpenAttribution/open-attribution"
				target="_blank"
				rel="noreferrer"
			>
				<div class="inline-flex items-center">
					{@html githubIcon}
					<h6 class="h6 p-2 justify-center text-center">Open Source on GitHub</h6>
				</div>
			</a>
		{/snippet}
	</AppBar>
</header>

<!--  Mobile only footer -->

<footer class="sticky bottom-0 z-10 bg-surface-50-950">
	<div class="md:hidden p-2">
		<!-- gridColumns="grid-cols-[auto_1fr_auto]" -->
		<AppBar padding="p-0">
			{#snippet lead()}
				<div class="inline-flex">
					<NavTabs />
				</div>
			{/snippet}
		</AppBar>
	</div>
</footer>

{@render children?.()}
