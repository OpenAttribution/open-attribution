<script lang="ts">
	let { children } = $props();
</script>

<div class="bg-muted/40 flex min-h-screen w-full flex-col">
	<div class="grid flex-1 items-start gap-4 p-4 px-8 md:px-32 py-16">
		{@render children()}
	</div>
</div>
