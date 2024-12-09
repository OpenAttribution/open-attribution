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
	<h2 class="h2">Create Link</h2>
	<div class="grid grid-cols-3 gap-6">
		<div class="col-span-1 text-lg">Domain</div>
		<Form.Field {form} name="domain" class="col-span-2">
			<div class={mainRowClass}>
				<div class={inputClass}>
					<Form.Control>
						{#snippet children({ props })}
							<Select.Root type="single" bind:value={$formData.domain_url} name={props.name}>
								<Select.Trigger {...props}>
									{$formData.domain_url ? $formData.domain_url : 'Select a domain to display'}
								</Select.Trigger>
								<Select.Content>
									{#each myDomains as domain}
										<Select.Item value={domain.domain_url} label={domain.domain_url} />
									{/each}
								</Select.Content>
							</Select.Root>
							<input
								type="hidden"
								name="domainId"
								value={myDomains.find((n: any) => n.domain_url === $formData.domain_url)?.id ?? ''}
							/>
						{/snippet}
					</Form.Control>
				</div>
				<Form.Description class="col-span-8">
					You can add custom domains in your <a href="/integrations/">integration setttings </a>.
				</Form.Description>
				<Form.FieldErrors />
			</div>
		</Form.Field>

		<div class="col-span-1 text-lg">URL Share ID</div>
		<Form.Field {form} name="shareSlug" class="col-span-2">
			<div class={mainRowClass}>
				<div class={inputClass}>
					<Form.Control>
						{#snippet children({ props })}
							<!-- <Form.Label class={labelClass}>URL Share ID</Form.Label> -->
							<Input {...props} bind:value={$formData.shareSlug} />
						{/snippet}
					</Form.Control>
				</div>
				<Form.Description class="col-span-8">
					Your app link's URL ID. If your id is 'tiktoksocial' it will correspond to
					'https://your.domain.com/s/tiktoksocial'. This will be tied this app but needs to be
					unique across your selected domain.
				</Form.Description>
			</div>
			<Form.FieldErrors />
		</Form.Field>

		<div class="col-span-1 text-lg">Network</div>
		<Form.Field {form} name="network" class="col-span-2">
			<div class={mainRowClass}>
				<div class={inputClass}>
					<Form.Control>
						{#snippet children({ props })}
							<!-- <Form.Label class={labelClass}>Network</Form.Label> -->
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
				</div>
				<Form.Description class="col-span-8">
					You can add custom network in your <a href="/integrations/">integration setttings </a>.
				</Form.Description>
				<Form.FieldErrors />
			</div>
		</Form.Field>

		<div class="col-span-1 text-lg">Android App</div>
		<Form.Field {form} name="androidAppId" class="col-span-2">
			<div class={mainRowClass}>
				<div class={inputClass}>
					<Form.Control>
						{#snippet children({ props })}
							<!-- <Form.Label class={labelClass}>Android App</Form.Label> -->
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
				</div>
				<Form.Description class="col-span-8">
					Your app link's URL ID. If your id is 'tiktoksocial' it will correspond to
					'https://your.domain.com/s/tiktoksocial'. This will be tied this app but needs to be
					unique across your selected domain.
				</Form.Description>
			</div>
			<Form.FieldErrors />
		</Form.Field>

		<div class="col-span-1 text-lg">iOS App</div>
		<Form.Field {form} name="iosAppId" class="col-span-2">
			<div class={mainRowClass}>
				<div class={inputClass}>
					<Form.Control>
						{#snippet children({ props })}
							<!-- <Form.Label class={labelClass}>iOS App</Form.Label> -->
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
				</div>
				<Form.Description class="col-span-8">
					Your app link's URL ID. If your id is 'tiktoksocial' it will correspond to
					'https://your.domain.com/s/tiktoksocial'. This will be tied this app but needs to be
					unique across your selected domain.
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
							<!-- <Form.Label class={labelClass}>Campaign Name</Form.Label> -->
							<Input {...props} bind:value={$formData.campaignName} />
						{/snippet}
					</Form.Control>
				</div>
				<Form.Description class="col-span-8">The campaign name you want to use.</Form.Description>
				<Form.FieldErrors />
			</div>
		</Form.Field>

		<div class="col-span-1 text-lg">Ad Name</div>
		<Form.Field {form} name="adName" class="col-span-2">
			<div class={mainRowClass}>
				<div class={inputClass}>
					<Form.Control>
						{#snippet children({ props })}
							<!-- <Form.Label class={labelClass}>Ad Name</Form.Label> -->
							<Input {...props} bind:value={$formData.adName} />
						{/snippet}
					</Form.Control>
				</div>
				<Form.Description class="col-span-8">The ad name you want to use.</Form.Description>
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
