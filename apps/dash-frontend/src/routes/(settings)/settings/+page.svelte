<script lang="ts">
	import { Button } from '$lib/components/ui/button/index';
	import * as Card from '$lib/components/ui/card/index';
	import { Checkbox } from '$lib/components/ui/checkbox/index';
	import { Input } from '$lib/components/ui/input/index';
</script>

<Card.Root>
	<Card.Header>
		<Card.Title>Store Name</Card.Title>
		<Card.Description>Used to identify your store in the marketplace.</Card.Description>
	</Card.Header>
	<Card.Content>
		<form>
			<Input placeholder="Store Name" />
		</form>
	</Card.Content>
	<Card.Footer class="border-t px-6 py-4">
		<Button>Save</Button>
	</Card.Footer>
</Card.Root>
<Card.Root>
	<Card.Header>
		<Card.Title>Plugins Directory</Card.Title>
		<Card.Description>
			The directory within your project, in which your plugins are located.
		</Card.Description>
	</Card.Header>
	<Card.Content>
		<form class="flex flex-col gap-4">
			<Input placeholder="Project Name" value="/content/plugins" />
			<div class="flex items-center space-x-2">
				<Checkbox id="include" checked={true} />
				<label
					for="include"
					class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
				>
					Allow administrators to change the directory.
				</label>
			</div>
		</form>
	</Card.Content>
	<Card.Footer class="border-t px-6 py-4">
		<Button>Save</Button>
	</Card.Footer>
</Card.Root>
