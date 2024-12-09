<script lang="ts">
	import * as Form from '$lib/components/ui/form';
	import { Input } from '$lib/components/ui/input';
	import { linkSchema, type LinkSchema } from '$schemas';
	import { type SuperValidated, type Infer, superForm } from 'sveltekit-superforms';
	import { zodClient } from 'sveltekit-superforms/adapters';
	import { Loader } from 'lucide-svelte';
	import { Button } from '$lib/components/ui/button';

	import IconAndroid from '$lib/svg/IconAndroid.svelte';
	import IconIOS from '$lib/svg/IconiOS.svelte';

	import * as Select from '$lib/components/ui/select';

	import { page } from '$app/stores';

	// export let data: SuperValidated<Infer<AppSchema>>;
	let { data, myApps, networks } = $props();
	type Message = { status: 'error' | 'success' | 'warning'; text: string };
	const form = superForm(data, {
		validators: zodClient(linkSchema),

		multipleSubmits: 'prevent'
	});

	const { form: formData, enhance, delayed, message } = form;
</script>

<form method="POST" use:enhance class="space-y-6" action="?/createLink">
	<h2 class="h2">Create Link</h2>
	<div class="grid grid-cols-1 gap-6">
		<!-- <input type="hidden" name="appId" value={appId} /> -->
		<input type="hidden" name="storeId" value={$page.params.storeid} />

		<Form.Field {form} name="shareSlug">
			<Form.Control>
				{#snippet children({ props })}
					<Form.Label>URL Share ID</Form.Label>
					<Input {...props} bind:value={$formData.shareSlug} />
				{/snippet}
			</Form.Control>
			<Form.Description
				>Your app link's URL ID. If your id is 'tiktoksocial' it will correspond to
				'https://your.domain.com/s/tiktoksocial'. This will be tied this app but needs to be unique
				across your selected domain.
			</Form.Description>
			<Form.FieldErrors />
		</Form.Field>

		<Form.Field {form} name="androidAppId">
			<Form.Control>
				{#snippet children({ props })}
					<Form.Label>Android App</Form.Label>
					<Select.Root type="single" bind:value={$formData.androidAppId} name={props.name}>
						<Select.Trigger {...props}>
							{$formData.androidAppId ? $formData.androidAppId : 'Select an android app'}
						</Select.Trigger>
						<Select.Content>
							{#each myApps as app}
								{#if app.store === 1}
									<Select.Item value={app.name} label={app.name}>
										<div class="flex items-center gap-2">
											{#if app.store === 1}
												<IconAndroid size="40" />
											{/if}
											{#if app.store === 2}
												<IconIOS size="40" />
											{/if}
											{app.name}
										</div>
									</Select.Item>
								{/if}
							{/each}
						</Select.Content>
					</Select.Root>
					<input
						type="hidden"
						name="androidAppId"
						value={myApps.find((n: any) => n.name === $formData.androidAppId)?.id ?? ''}
					/>
				{/snippet}
			</Form.Control>
		</Form.Field>

		<Form.Field {form} name="iosAppId">
			<Form.Control>
				{#snippet children({ props })}
					<Form.Label>iOS App</Form.Label>
					<Select.Root type="single" bind:value={$formData.iosAppId} name={props.name}>
						<Select.Trigger {...props}>
							{$formData.iosAppId ? $formData.iosAppId : 'Select an iOS app'}
						</Select.Trigger>
						<Select.Content>
							{#each myApps as app}
								{#if app.store === 2}
									<Select.Item value={app.name} label={app.name}>
										<div class="flex items-center gap-2">
											{#if app.store === 1}
												<IconAndroid size="50" />
											{/if}
											{#if app.store === 2}
												<IconIOS size="40" />
											{/if}
											{app.name}
										</div>
									</Select.Item>
								{/if}
							{/each}
						</Select.Content>
					</Select.Root>
					<input
						type="hidden"
						name="iosAppId"
						value={myApps.find((n: any) => n.name === $formData.iosAppId)?.id ?? ''}
					/>
				{/snippet}
			</Form.Control>
		</Form.Field>

		<Form.Field {form} name="network">
			<Form.Control>
				{#snippet children({ props })}
					<Form.Label>Network</Form.Label>
					<Select.Root type="single" bind:value={$formData.network} name={props.name}>
						<Select.Trigger {...props}>
							{$formData.network ? $formData.network : 'Select a network to display'}
						</Select.Trigger>
						<Select.Content>
							{#each networks as network}
								<Select.Item value={network.name} label={network.name} />
							{/each}
						</Select.Content>
					</Select.Root>
					<input
						type="hidden"
						name="networkId"
						value={networks.find((n: any) => n.name === $formData.network)?.id ?? ''}
					/>
				{/snippet}
			</Form.Control>

			<Form.Description>
				You can add custom network in your <a href="/integrations/">integration setttings</a>.
			</Form.Description>
			<Form.FieldErrors />
		</Form.Field>

		<Form.Field {form} name="campaignName">
			<Form.Control>
				{#snippet children({ props })}
					<Form.Label>Campaign Name</Form.Label>
					<Input {...props} bind:value={$formData.campaignName} />
				{/snippet}
			</Form.Control>
			<Form.Description>The campaign name you want to use.</Form.Description>
			<Form.FieldErrors />
		</Form.Field>

		<Form.Field {form} name="adName">
			<Form.Control>
				{#snippet children({ props })}
					<Form.Label>Ad Name</Form.Label>
					<Input {...props} bind:value={$formData.adName} />
				{/snippet}
			</Form.Control>
			<Form.Description>The ad name you want to use.</Form.Description>
			<Form.FieldErrors />
		</Form.Field>
		<Button type="submit" class="w-full">Submit</Button>
		{#if $delayed}
			<Loader></Loader>
		{/if}

		{#if $message}
			<div class="error">
				<p>{$message}</p>
			</div>
		{/if}

		<style>
			.error {
				color: red;
				margin-top: 1rem;
			}
		</style>
	</div>
</form>
