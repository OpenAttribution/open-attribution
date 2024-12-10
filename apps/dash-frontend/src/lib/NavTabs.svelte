<script lang="ts">
	import { Blocks, Settings, Link } from 'lucide-svelte';
	import LineChart from 'lucide-svelte/icons/chart-column';
</script>

<nav
	class="hidden flex-col gap-6 text-lg font-medium md:flex md:flex-row md:items-center md:gap-5 md:text-sm lg:gap-6"
>
	<a href="/" class="flex items-center gap-2 text-lg font-semibold md:text-base">
		<span class="">OpenAttribution</span>
	</a>

	<a href="/" class="flex text-muted-foreground hover:text-foreground transition-colors"
		><LineChart /> Dashboard
	</a>
	<a
		href="/integrations"
		class="flex text-muted-foreground hover:text-foreground transition-colors"
	>
		<Blocks />
		Network Integrations
	</a>

	<a
		href="/settings/apps"
		class="flex text-muted-foreground hover:text-foreground transition-colors"
	>
		<Settings />
		Apps
	</a>
	<a href="/links" class="flex text-muted-foreground hover:text-foreground transition-colors">
		<Link />
		Links
	</a>

	<!-- <a
		href="/settings/general"
		class="flex text-muted-foreground hover:text-foreground transition-colors"
	>
		<Settings />
		Settings
	</a> -->
</nav>
