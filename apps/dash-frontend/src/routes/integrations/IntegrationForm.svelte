<script lang="ts">
	import { Input } from '$lib/components/ui/input';
	import { Button } from '$lib/components/ui/button';
	import { redirect } from '@sveltejs/kit';

	import * as Form from '$lib/components/ui/form/index.js';
	import { networkSchema, type NetworkSchema } from '$schemas';
	import { type SuperValidated, type Infer, superForm } from 'sveltekit-superforms';
	import { zodClient } from 'sveltekit-superforms/adapters';

	export let data: SuperValidated<Infer<NetworkSchema>>;

	export let success: () => void;

	const form = superForm(data, {
		validators: zodClient(networkSchema)
	});

	const { form: formData, enhance, message } = form;
</script>

<form class="grid items-start gap-4 px-4" method="POST" action="?/createIntegration" use:enhance>
	<div class="grid gap-2">
		<Form.Field {form} name="networkName">
			<Form.Control>
				{#snippet children({ props })}
					<Form.Label>Name</Form.Label>
					<Input {...props} bind:value={$formData.networkName} />
				{/snippet}
			</Form.Control>
			<Form.Description>This is the display name of your custom network.</Form.Description>
			<Form.FieldErrors />
		</Form.Field>
		<Form.Field {form} name="postbackId">
			<Form.Control>
				{#snippet children({ props })}
					<Form.Label>Postback ID</Form.Label>
					<Input {...props} bind:value={$formData.postbackId} />
				{/snippet}
			</Form.Control>
			<Form.Description
				>This is the urlsafe identifier of your custom network. Underscores and dashes OK.</Form.Description
			>
			<Form.FieldErrors />
		</Form.Field>

		<Button type="submit">Save changes</Button>
		{#if $message}
			{#if $message === 'success'}
				{success()}
			{:else}
				<div class="message">{$message}</div>
			{/if}
		{/if}
	</div>
</form>
