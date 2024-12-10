<script>
	import '../app.css';
	import CircleUser from 'lucide-svelte/icons/circle-user';
	import { Button } from '$lib/components/ui/button/index';
	import Sun from 'lucide-svelte/icons/sun';
	import Moon from 'lucide-svelte/icons/moon';
	import * as DropdownMenu from '$lib/components/ui/dropdown-menu/index';
	import { ModeWatcher, toggleMode } from 'mode-watcher';
	import NavTabs from '$lib/NavTabs.svelte';
	let { children } = $props();
</script>

<ModeWatcher defaultMode={'dark'}></ModeWatcher>

<header class="bg-background sticky top-0 z-30 flex h-16 items-center gap-4 border-b px-4 md:px-6">
	<NavTabs />
	<div class="flex w-full items-center gap-4 md:ml-auto md:gap-2 lg:gap-4">
		<div class="ml-auto flex-1 sm:flex-initial">
			<div class="relative"></div>
		</div>

		<DropdownMenu.Root>
			<DropdownMenu.Trigger>
				<Button variant="secondary" size="icon" class="rounded-full">
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

	<Button onclick={toggleMode} variant="outline" size="icon">
		<Sun
			class="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0"
		/>
		<Moon
			class="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100"
		/>
		<span class="sr-only">Toggle theme</span>
	</Button>
</header>

{@render children()}
