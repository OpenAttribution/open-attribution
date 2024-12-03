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
		<!-- <AppBar
			leadBase="p-2 md:items-center"
			trailBase="p-2 items-center"
			centerBase="hidden md:flex items-center"
			padding="p-0"
		> -->
		<AppBar padding="p-1 sm:p-2 md:p-4" centerClasses="hidden md:flex">
			{#snippet lead()}
				<a href="/">
					<strong class="ml-4 text-xl md:text-2xl uppercase break-words justify-start"
						>Open Attribution</strong
					>
				</a>
			{/snippet}

			<div class="items-center justify-center">
				<NavTabs />
			</div>

			{#snippet trail()}
				<div class="flex flex-col lg:flex-row gap-2 md:gap-4">
					<a
						class="btn preset-outlined-primary-900-100 p-2 md:p-4"
						href="mailto:hello@openattribution.dev"
					>
						Email Contact
					</a>
					<div class="grid grid-cols-2 gap-2 md:gap-4">
						<a
							class="btn preset-outlined-tertiary-500 p-2 md:p-4"
							href="https://discord.gg/Z5ueYE3Ct3"
							target="_blank"
							rel="noreferrer"
						>
							<div class="h-4 md:h-8 w-full flex items-center">
								{@html discordIcon}
							</div>
						</a>
						<a
							class="btn preset-outlined-tertiary-500 p-2 md:p-4"
							href="https://github.com/OpenAttribution/open-attribution"
							target="_blank"
							rel="noreferrer"
						>
							<div class="flex items-center gap-2">
								<div class="h-4 w-4 md:h-8 md:w-8 md:p-1">
									{@html githubIcon}
								</div>
								<h6 class="h6 text-center">GitHub</h6>
							</div>
						</a>
					</div>
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
