<script lang="ts">
	import { Input } from '$lib/components/ui/input';
	import { Button } from '$lib/components/ui/button';

	import * as Form from '$lib/components/ui/form/index.js';
	import { domainSchema, type DomainSchema } from '$schemas';
	import { type SuperValidated, type Infer, superForm } from 'sveltekit-superforms';
	import { zodClient } from 'sveltekit-superforms/adapters';

	export let data: SuperValidated<Infer<DomainSchema>>;

	export let success: () => void;

	const form = superForm(data, {
		validators: zodClient(domainSchema)
	});

	const { form: formData, enhance, message } = form;
</script>

<form class="grid items-start gap-4 px-4" method="POST" action="?/createClientDomain" use:enhance>
	<div class="grid gap-2">
		https://<Form.Field {form} name="clientDomain">
			<Form.Control>
				{#snippet children({ props })}
					<Form.Label>Domain</Form.Label>
					<Input {...props} bind:value={$formData.clientDomain} />
				{/snippet}
			</Form.Control>
			<Form.Description>This is the display name of your custom network.</Form.Description>
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
