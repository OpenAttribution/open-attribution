<script lang="ts">
	import { browser } from '$app/environment';
	import * as Dialog from '$lib/components/ui/dialog/index.js';
	import * as Drawer from '$lib/components/ui/drawer/index.js';
	import { buttonVariants } from '$lib/components/ui/button/index.js';

	import IntegrationForm from '$lib/CreateIntegrationForm.svelte';

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
		<Dialog.Trigger class={buttonVariants({ variant: 'outline' })}
			>Add Custom Network</Dialog.Trigger
		>
		<Dialog.Content class="sm:max-w-[425px]">
			<Dialog.Header>
				<Dialog.Title>Add Custom Network</Dialog.Title>
				<Dialog.Description>
					Add your custom ad network or channel. Example: Name: My Cross Promotion Postback ID:
					my_cross_promotion
				</Dialog.Description>
			</Dialog.Header>
			<IntegrationForm data={data.form} success={() => (open = false)} />
		</Dialog.Content>
	</Dialog.Root>
{:else}
	<Drawer.Root bind:open>
		<Drawer.Trigger class={buttonVariants({ variant: 'outline' })}
			>Add Custom Network</Drawer.Trigger
		>
		<Drawer.Content>
			<Drawer.Header class="text-left">
				<Drawer.Title>Add Custom Network</Drawer.Title>
				<Drawer.Description>
					Add your custom ad network or channel. Example: Name: My Cross Promotion Postback ID:
					my_cross_promotion
				</Drawer.Description>
			</Drawer.Header>
			<IntegrationForm data={data.form} success={() => (open = false)} />
			<Drawer.Footer class="pt-2">
				<Drawer.Close class={buttonVariants({ variant: 'outline' })}>Cancel</Drawer.Close>
			</Drawer.Footer>
		</Drawer.Content>
	</Drawer.Root>
{/if}
