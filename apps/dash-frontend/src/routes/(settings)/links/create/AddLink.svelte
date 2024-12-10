<script lang="ts">
	import * as Form from '$lib/components/ui/form';
	import { Input } from '$lib/components/ui/input';
	import { linkSchema } from '$schemas';
	import { superForm } from 'sveltekit-superforms';
	import { zodClient } from 'sveltekit-superforms/adapters';
	import { Loader } from 'lucide-svelte';
	import { Button } from '$lib/components/ui/button';

	import IconAndroid from '$lib/svg/IconAndroid.svelte';
	import IconIOS from '$lib/svg/IconiOS.svelte';

	import * as Select from '$lib/components/ui/select';

	let { data, myApps, networks, myDomains } = $props();

	const form = superForm(data, {
		validators: zodClient(linkSchema),

		multipleSubmits: 'prevent'
	});

	const { form: formData, enhance, delayed, message } = form;

	const mainRowClass = 'grid grid-cols-12 gap-4 w-full';
	const inputClass = 'col-span-4';
</script>

<form method="POST" use:enhance class="space-y-6 px-16" action="?/createLink">
	<h2 class="h2">
		Creating Share URL:
		<span class="text-gray-500">
			{#if !$formData.domain_url && !$formData.shareSlug}
				https://
			{/if}
			{#if $formData.domain_url && !$formData.shareSlug}
				https://{$formData.domain_url}/
			{/if}
			{#if $formData.domain_url && $formData.shareSlug}
				https://{$formData.domain_url}/{$formData.shareSlug}
			{/if}
		</span>
	</h2>
	<div class="grid grid-cols-3 gap-6">
		<div class="col-span-1 text-lg">Domain</div>
		<Form.Field {form} name="domainId" class="col-span-2">
			<div class={mainRowClass}>
				<div class={inputClass}>
					<Form.Control>
						{#snippet children({ props })}
							<Select.Root type="single" bind:value={$formData.domainId} name={props.name}>
								<Select.Trigger {...props}>
									{$formData.domainId
										? myDomains.find((domain: any) => domain.db_id === $formData.domainId)
												?.domain_url
										: 'Select a domain to display'}
								</Select.Trigger>
								<Select.Content>
									{#each myDomains as domain}
										<Select.Item value={domain.db_id} label={domain.domain_url} />
									{/each}
								</Select.Content>
							</Select.Root>
						{/snippet}
					</Form.Control>
				</div>
				<Form.Description class="col-span-8">
					You can add custom domains in your <a href="/integrations/">integration setttings </a>.
					Stored in database and associated with the URL you choose.
				</Form.Description>
				<Form.FieldErrors />
			</div>
		</Form.Field>

		<div class="col-span-1 text-lg">
			<div class="text-lg">URL Suffix</div>
		</div>
		<Form.Field {form} name="shareSlug" class="col-span-2">
			<div class={mainRowClass}>
				<div class={inputClass}>
					<Form.Control>
						{#snippet children({ props })}
							<Input {...props} bind:value={$formData.shareSlug} />
							<Form.Label class="text-sm">eg: {$formData.shareSlug} URL Share ID</Form.Label>
						{/snippet}
					</Form.Control>
				</div>
				<Form.Description class="col-span-8">
					Your share link's URL suffix slug. Can be 1-50 characters. This value must be urlsafe.
					Shorter is better for sharing. If your slug is 'fb' it will correspond to
					'https://your.domain.com/fb'. This will need to be unique across your selected domain.
				</Form.Description>
			</div>
			<Form.FieldErrors />
		</Form.Field>

		<div class="col-span-1 text-lg">Network</div>
		<Form.Field {form} name="networkId" class="col-span-2">
			<div class={mainRowClass}>
				<div class={inputClass}>
					<Form.Control>
						{#snippet children({ props })}
							<Select.Root type="single" bind:value={$formData.networkId} name={props.name}>
								<Select.Trigger {...props}>
									{$formData.networkId
										? networks.find((network: any) => network.id === $formData.networkId)?.name
										: 'Select a network to display'}
								</Select.Trigger>
								<Select.Content>
									{#each networks as network}
										<Select.Item value={network.id} label={network.name} />
									{/each}
								</Select.Content>
							</Select.Root>
						{/snippet}
					</Form.Control>
				</div>
				<Form.Description class="col-span-8">
					You can add new custom networks in <a href="/integrations/">integration setttings</a>.
				</Form.Description>
				<Form.FieldErrors />
			</div>
		</Form.Field>

		<div class="col-span-1 text-lg">Google Android App</div>
		<Form.Field {form} name="googleAppId" class="col-span-2">
			<div class={mainRowClass}>
				<div class={inputClass}>
					<Form.Control>
						{#snippet children({ props })}
							<Select.Root type="single" bind:value={$formData.googleAppId} name={props.name}>
								<Select.Trigger {...props}>
									<IconAndroid size="40" />
									{$formData.googleAppId
										? myApps.find((app: any) => app.id === $formData.googleAppId)?.name
										: 'Select an android app'}
								</Select.Trigger>
								<Select.Content>
									{#each myApps as app}
										{#if app.store === 1}
											<Select.Item value={app.id} label={app.name}>
												<div class="flex items-center gap-2">
													<IconAndroid size="40" />
													{app.name}
												</div>
											</Select.Item>
										{/if}
									{/each}
								</Select.Content>
							</Select.Root>
						{/snippet}
					</Form.Control>
				</div>
				<Form.Description class="col-span-8">
					Optional. The Google Play Store App you'd like to redirect to when Android is detected.
				</Form.Description>
			</div>
			<Form.FieldErrors />
		</Form.Field>

		<div class="col-span-1 text-lg">iOS App</div>
		<Form.Field {form} name="appleAppId" class="col-span-2">
			<div class={mainRowClass}>
				<div class={inputClass}>
					<Form.Control>
						{#snippet children({ props })}
							<Select.Root type="single" bind:value={$formData.appleAppId} name={props.name}>
								<Select.Trigger {...props}>
									<IconIOS size="40" />
									{$formData.appleAppId
										? myApps.find((app: any) => app.id === $formData.appleAppId)?.name
										: 'Select an iOS app'}
								</Select.Trigger>
								<Select.Content>
									{#each myApps as app}
										{#if app.store === 2}
											<Select.Item value={app.id} label={app.name}>
												<div class="flex items-center gap-2">
													<IconIOS size="40" />
													{app.name}
												</div>
											</Select.Item>
										{/if}
									{/each}
								</Select.Content>
							</Select.Root>
						{/snippet}
					</Form.Control>
				</div>
				<Form.Description class="col-span-8">
					Optional. The iOS App you'd like to redirect to when iOS is detected.
				</Form.Description>
			</div>
			<Form.FieldErrors />
		</Form.Field>

		<div class="col-span-1 text-lg">Campaign Name</div>
		<Form.Field {form} name="campaignName" class="col-span-2">
			<div class={mainRowClass}>
				<div class={inputClass}>
					<Form.Control>
						{#snippet children({ props })}
							<Input {...props} bind:value={$formData.campaignName} />
						{/snippet}
					</Form.Control>
				</div>
				<Form.Description class="col-span-8"
					>2 - 50 characters. The campaign name you want to use. This is stored in the backend and
					will be associated with the URL you choose.</Form.Description
				>
				<Form.FieldErrors />
			</div>
		</Form.Field>

		<div class="col-span-1 text-lg">Ad Name</div>
		<Form.Field {form} name="adName" class="col-span-2">
			<div class={mainRowClass}>
				<div class={inputClass}>
					<Form.Control>
						{#snippet children({ props })}
							<Input {...props} bind:value={$formData.adName} />
						{/snippet}
					</Form.Control>
				</div>
				<Form.Description class="col-span-8"
					>Optional. 2-50 characters. The ad name you want to use. Stored in the backend and
					associated with the URL you choose.</Form.Description
				>
				<Form.FieldErrors />
			</div>
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
