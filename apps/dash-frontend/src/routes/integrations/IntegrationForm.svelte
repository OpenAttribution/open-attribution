<script lang="ts">
	import { Label } from '$lib/components/ui/label';
	import { Input } from '$lib/components/ui/input';
	import { Button } from '$lib/components/ui/button';
</script>

<form class="grid items-start gap-4 px-4" method="POST" action="?/integrations">
	<div class="grid gap-2">
		<div class="grid grid-cols-3 items-center gap-4">
			<Label for="name">Name</Label>
			<Input id="name" name="name" value="Name..." class="col-span-2 h-8" />
		</div>
		<div class="grid grid-cols-3 items-center gap-4">
			<Label for="postback_id">Postback ID</Label>
			<Input id="postback_id" name="postback_id" value="postback_id..." class="col-span-2 h-8" />
		</div>

		<Button type="submit">Save changes</Button>
	</div>
</form>
