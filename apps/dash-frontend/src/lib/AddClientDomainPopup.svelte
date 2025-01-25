<script lang="ts">
	import { browser } from '$app/environment';
	import * as Dialog from '$lib/components/ui/dialog/index.js';
	import * as Drawer from '$lib/components/ui/drawer/index.js';
	import { buttonVariants } from '$lib/components/ui/button/index.js';

	import CreateDomainForm from '$lib/CreateDomainForm.svelte';

	let open = false;
	let isDesktop = false;

	// Only run this code on the client side
	$: if (browser) {
		isDesktop = window.innerWidth >= 768;
		window.addEventListener('resize', () => {
			isDesktop = window.innerWidth >= 768;
		});
	}

	export let data;
</script>

{#if isDesktop}
	<Dialog.Root bind:open>
		<Dialog.Trigger class={buttonVariants({ variant: 'outline' })}>Add Client Domain</Dialog.Trigger
		>
		<Dialog.Content class="sm:max-w-[425px]">
			<Dialog.Header>
				<Dialog.Title>Add Client Domain</Dialog.Title>
				<Dialog.Description>
					Add your custom client domain. Example: oa.mydomain.com
				</Dialog.Description>
			</Dialog.Header>
			<CreateDomainForm data={data.form} success={() => (open = false)} />
		</Dialog.Content>
	</Dialog.Root>
{:else}
	<Drawer.Root bind:open>
		<Drawer.Trigger class={buttonVariants({ variant: 'outline' })}>Add Client Domain</Drawer.Trigger
		>
		<Drawer.Content>
			<Drawer.Header class="text-left">
				<Drawer.Title>Add Client Domain</Drawer.Title>
				<Drawer.Description>
					Add your custom client domain. Example: oa.mydomain.com
				</Drawer.Description>
			</Drawer.Header>
			<CreateDomainForm data={data.form} success={() => (open = false)} />
			<Drawer.Footer class="pt-2">
				<Drawer.Close class={buttonVariants({ variant: 'outline' })}>Cancel</Drawer.Close>
			</Drawer.Footer>
		</Drawer.Content>
	</Drawer.Root>
{/if}
