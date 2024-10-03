<script lang="ts">
	import * as Form from '$lib/components/ui/form';
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';
	import * as RadioGroup from '$lib/components/ui/radio-group';
	import { formSchema, type FormSchema } from './schema';
	import { type SuperValidated, type Infer, superForm } from 'sveltekit-superforms';
	import { zodClient } from 'sveltekit-superforms/adapters';

	export let data: SuperValidated<Infer<FormSchema>>;

	const form = superForm(data, {
		validators: zodClient(formSchema)
	});

	const { form: formData, enhance } = form;
</script>

<form method="POST" use:enhance>
	<Form.Field {form} name="appName">
		<Form.Control let:attrs>
			<Form.Label>App Name</Form.Label>
			<Input {...attrs} bind:value={$formData.appName} />
		</Form.Control>
		<Form.Description>Your app's display name.</Form.Description>
		<Form.FieldErrors />
	</Form.Field>
	<Form.Field {form} name="storeId">
		<Form.Control let:attrs>
			<Form.Label>Store ID</Form.Label>
			<Input {...attrs} bind:value={$formData.storeId} />
		</Form.Control>
		<Form.Description>
			Store ID. iOS example: "1234567890" Android: "com.example.app"
		</Form.Description>
		<Form.FieldErrors />
	</Form.Field>
	<Form.Field {form} name="appStore">
		<Form.Control let:attrs>
			<Form.Label>App Store</Form.Label>
			<Input {...attrs} bind:value={$formData.appStore} />
			<RadioGroup.Root value="comfortable">
				<div class="flex items-center space-x-2">
					<RadioGroup.Item value="default" id="r1" />
					<Label for="r1">Default</Label>
				</div>
				<div class="flex items-center space-x-2">
					<RadioGroup.Item value="comfortable" id="r2" />
					<Label for="r2">Comfortable</Label>
				</div>
				<div class="flex items-center space-x-2">
					<RadioGroup.Item value="compact" id="r3" />
					<Label for="r3">Compact</Label>
				</div>
				<RadioGroup.Input name="spacing" />
			</RadioGroup.Root>
		</Form.Control>
		<Form.Description>Select which app store your app is live on.</Form.Description>
		<Form.FieldErrors />
	</Form.Field>
	<Form.Button>Submit</Form.Button>
</form>
