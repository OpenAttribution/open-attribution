<script>
	import '../app.css';
	import Menu from 'lucide-svelte/icons/menu';
	import Package2 from 'lucide-svelte/icons/package-2';
	import CircleUser from 'lucide-svelte/icons/circle-user';
	import { Button } from '$lib/components/ui/button/index';
	import Sun from 'lucide-svelte/icons/sun';
	import Moon from 'lucide-svelte/icons/moon';
	import * as DropdownMenu from '$lib/components/ui/dropdown-menu/index';
	import * as Sheet from '$lib/components/ui/sheet/index';
	import LineChart from 'lucide-svelte/icons/chart-column';
	import { Blocks } from 'lucide-svelte';
	import { ModeWatcher, toggleMode } from 'mode-watcher';
</script>

<ModeWatcher defaultMode={'dark'}></ModeWatcher>

<header class="bg-background sticky top-0 flex h-16 items-center gap-4 border-b px-4 md:px-6">
	<nav
		class="hidden flex-col gap-6 text-lg font-medium md:flex md:flex-row md:items-center md:gap-5 md:text-sm lg:gap-6"
	>
		<a href="##" class="flex items-center gap-2 text-lg font-semibold md:text-base">
			<span class="">OpenAttribution</span>
		</a>

		<a href="/" class="flex text-muted-foreground hover:text-foreground transition-colors"
			><LineChart></LineChart> Dashboard
		</a>
		<a
			href="/integrations"
			class="flex text-muted-foreground hover:text-foreground transition-colors"
		>
			<Blocks></Blocks>
			Integrations
		</a>
	</nav>
	<Sheet.Root>
		<Sheet.Trigger asChild let:builder>
			<Button variant="outline" size="icon" class="shrink-0 md:hidden" builders={[builder]}>
				<Menu class="h-5 w-5" />
				<span class="sr-only">Toggle navigation menu</span>
			</Button>
		</Sheet.Trigger>
		<Sheet.Content side="left">
			<nav class="grid gap-6 text-lg font-medium">
				<a href="##" class="flex items-center gap-2 text-lg font-semibold">
					<Package2 class="h-6 w-6" />
					<span class="sr-only">Acme Inc</span>
				</a>
				<a href="##" class="hover:text-foreground"> Dashboard </a>
				<a href="##" class="text-muted-foreground hover:text-foreground"> Orders </a>
				<a href="##" class="text-muted-foreground hover:text-foreground"> Products </a>
				<a href="##" class="text-muted-foreground hover:text-foreground"> Customers </a>
				<a href="##" class="text-muted-foreground hover:text-foreground"> Analytics </a>
			</nav>
		</Sheet.Content>
	</Sheet.Root>
	<div class="flex w-full items-center gap-4 md:ml-auto md:gap-2 lg:gap-4">
		<div class="ml-auto flex-1 sm:flex-initial">
			<div class="relative"></div>
		</div>
		<DropdownMenu.Root>
			<DropdownMenu.Trigger asChild let:builder>
				<Button builders={[builder]} variant="secondary" size="icon" class="rounded-full">
					<CircleUser class="h-5 w-5" />
					<span class="sr-only">Toggle user menu</span>
				</Button>
			</DropdownMenu.Trigger>
			<DropdownMenu.Content align="end">
				<DropdownMenu.Label><a href="/account">My Account</a></DropdownMenu.Label>
				<DropdownMenu.Separator />
				<DropdownMenu.Item><a href="/settings/general">Settings</a></DropdownMenu.Item>
				<DropdownMenu.Item><a href="/support">Support</a></DropdownMenu.Item>
				<DropdownMenu.Separator />
				<DropdownMenu.Item>Logout</DropdownMenu.Item>
			</DropdownMenu.Content>
		</DropdownMenu.Root>
	</div>

	<Button on:click={toggleMode} variant="outline" size="icon">
		<Sun
			class="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0"
		/>
		<Moon
			class="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100"
		/>
		<span class="sr-only">Toggle theme</span>
	</Button>
</header>

<slot />
