<script lang="ts">
	let { children } = $props();
</script>

<div class="flex min-h-screen w-full flex-col">
	<main
		class="bg-muted/40 flex min-h-[calc(100vh_-_theme(spacing.16))] flex-1 flex-col gap-4 p-4 md:gap-8 md:p-10"
	>
		<div class="mx-auto grid w-full max-w-6xl gap-2">
			<h1 class="text-3xl font-semibold">Settings</h1>
		</div>
		<div
			class="mx-auto grid w-full max-w-6xl items-start gap-6 md:grid-cols-[180px_1fr] lg:grid-cols-[250px_1fr]"
		>
			<nav
				class="text-muted-foreground grid gap-4 text-sm"
				data-x-chunk-container="chunk-container after:right-0"
			>
				<a href="/settings/general" class="text-primary font-semibold"> General </a>
				<a href="/settings/apps">Apps</a>
				<a href="/settings/team">Team</a>
			</nav>
			<div class="grid gap-6">
				{@render children()}
			</div>
		</div>
	</main>
</div>
