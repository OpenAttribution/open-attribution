<script lang="ts">
	import NavTabs from '$lib/NavTabs.svelte';
	import '../app.postcss';
	import { AppShell, AppBar } from '@skeletonlabs/skeleton';
	import githubIcon from '$lib/assets/github-mark-white.svg?raw';
</script>

<!-- App Shell -->
<AppShell>
	<!-- Large only header -->
	<svelte:fragment slot="header">
		<!-- App Bar -->
		<AppBar
			gridColumns="grid-cols-[1fr_0_1fr] md:grid-cols-[0.4fr_1fr_0.3fr]"
			slotLead="p-2"
			slotTrail="p-2"
			spacing="space-y-0"
			padding="p-0"
		>
			<svelte:fragment slot="lead">
				<strong class=" ml-4 text- xl md:text-2xl uppercase">Open Attribution</strong>
			</svelte:fragment>

			<div class="hidden lg:inline-flex">
				<NavTabs />
			</div>

			<svelte:fragment slot="trail">
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
			</svelte:fragment>
		</AppBar>
	</svelte:fragment>

	<!--  Mobile only footer -->
	<svelte:fragment slot="footer">
		<AppBar
			slotLead="p-0"
			slotTrail="p-2"
			spacing="space-y-0"
			padding="p-0"
			gap="gap-0"
			class="lg:hidden"
			gridColumns="grid-cols-[auto_1fr_auto]"
		>
			<svelte:fragment slot="lead">
				<div class="inline-flex">
					<NavTabs />
				</div>
			</svelte:fragment>
		</AppBar>
	</svelte:fragment>

	<!-- Page Route Content -->
	<slot />
</AppShell>
