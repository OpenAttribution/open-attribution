<script lang="ts">
	import { Checkbox } from '$lib/components/ui/checkbox';
	import { Button } from '$lib/components/ui/button';
	import * as Popover from '$lib/components/ui/popover';
	import { Check, ChevronsUpDown } from 'lucide-svelte';
	import { fly } from 'svelte/transition';
	import { createEventDispatcher } from 'svelte';

	export let options: { value: string; label: string }[] = [];
	export let placeholder = 'Select options...';

	let selected: string[] = [];
	let open = false;

	const dispatch = createEventDispatcher();

	function toggleOption(value: string) {
		if (selected.includes(value)) {
			selected = selected.filter((v) => v !== value);
		} else {
			selected = [...selected, value];
		}
		dispatch('change', selected);
	}

	function getLabel(value: string) {
		return options.find((option) => option.value === value)?.label || value;
	}

	function handleKeyDown(event: KeyboardEvent, value: string) {
		if (event.key === 'Enter' || event.key === ' ') {
			event.preventDefault();
			toggleOption(value);
		}
	}
</script>

<Popover.Root bind:open>
	<Popover.Trigger asChild let:builder>
		<Button
			variant="outline"
			role="combobox"
			aria-expanded={open}
			class="w-full justify-between"
			builders={[builder]}
		>
			{#if selected.length === 0}
				<span class="text-muted-foreground">{placeholder}</span>
			{:else}
				<span class="truncate">
					{selected.map(getLabel).join(', ')}
				</span>
			{/if}
			<ChevronsUpDown class="ml-2 h-4 w-4 shrink-0 opacity-50" />
		</Button>
	</Popover.Trigger>
	<Popover.Content class="w-[--radix-popover-trigger-width] p-0">
		<div role="listbox" class="max-h-[300px] overflow-auto">
			{#each options as option (option.value)}
				<div
					role="option"
					aria-selected={selected.includes(option.value)}
					tabindex="0"
					class="relative flex cursor-default select-none items-center rounded-sm px-2 py-1.5 text-sm outline-none hover:bg-accent hover:text-accent-foreground focus:bg-accent focus:text-accent-foreground data-[disabled]:pointer-events-none data-[disabled]:opacity-50"
					on:click={() => toggleOption(option.value)}
					on:keydown={(event) => handleKeyDown(event, option.value)}
					transition:fly={{ y: -5, duration: 200 }}
				>
					<Checkbox checked={selected.includes(option.value)} class="mr-2" />
					<span>{option.label}</span>
					{#if selected.includes(option.value)}
						<Check class="ml-auto h-4 w-4" />
					{/if}
				</div>
			{/each}
		</div>
	</Popover.Content>
</Popover.Root>
