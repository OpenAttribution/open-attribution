<script lang="ts">
	import * as Form from '$lib/components/ui/form';
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';
	import * as RadioGroup from '$lib/components/ui/radio-group';
	import { appSchema, type AppSchema } from '$schemas';
	import { type SuperValidated, type Infer, superForm } from 'sveltekit-superforms';
	import { zodClient } from 'sveltekit-superforms/adapters';
	import { Loader } from 'lucide-svelte';
	import { Button } from '$lib/components/ui/button';

	// export let data: SuperValidated<Infer<AppSchema>>;
	let { data } = $props();
	type Message = { status: 'error' | 'success' | 'warning'; text: string };
	const form = superForm(data, {
		validators: zodClient(appSchema),

		multipleSubmits: 'prevent'
	});

	const { form: formData, enhance, delayed, message } = form;
</script>

<form method="POST" use:enhance class="space-y-6" action="?/createApp">
	<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
		<Form.Field {form} name="appName">
			<Form.Control>
				{#snippet children({ props })}
					<Form.Label>App Name</Form.Label>
					<Input {...props} bind:value={$formData.appName} />
				{/snippet}
			</Form.Control>
			<Form.Description>Your app's display name.</Form.Description>
			<Form.FieldErrors />
		</Form.Field>

		<Form.Field {form} name="storeId">
			<Form.Control>
				{#snippet children({ props })}
					<Form.Label>Store ID</Form.Label>
					<Input {...props} bind:value={$formData.storeId} />
				{/snippet}
			</Form.Control>
			<Form.Description>
				Store ID. iOS example: "1234567890" Android: "com.example.app"
			</Form.Description>
			<Form.FieldErrors />
		</Form.Field>

		<Form.Field {form} name="appStore" class="col-span-full">
			<Form.Control>
				<Form.Label>App Store</Form.Label>
				<RadioGroup.Root
					bind:value={$formData.appStore}
					class="flex flex-col space-y-2"
					name="appStore"
				>
					<div class="flex items-center space-x-2">
						<RadioGroup.Item value="ios" id="ios" />
						<Label for="ios">iOS App Store</Label>
					</div>
					<div class="flex items-center space-x-2">
						<RadioGroup.Item value="android" id="android" />
						<Label for="android">Google Play Store</Label>
					</div>
				</RadioGroup.Root>
			</Form.Control>
			<Form.Description>Select the app store.</Form.Description>
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
