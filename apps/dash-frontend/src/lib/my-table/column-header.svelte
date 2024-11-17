<!-- <script lang="ts" module>
	type TData = unknown;
	type TValue = unknown;
</script> -->

<!-- <script lang="ts" generics="TData, TValue"> -->
<script lang="ts">
	import ArrowDown from 'lucide-svelte/icons/chevron-down';
	import ArrowUp from 'lucide-svelte/icons/chevron-up';
	import CaretSort from 'lucide-svelte/icons/chevrons-up-down';
	// import type { HTMLAttributes } from 'svelte/elements';
	import type { Column } from '@tanstack/table-core';
	import type { WithoutChildren } from 'bits-ui';
	import { cn } from '$lib/utils.js';
	import * as DropdownMenu from '$lib/components/ui/dropdown-menu/index.js';
	import { Button } from '$lib/components/ui/button/index.js';

	// type Props = HTMLAttributes<HTMLDivElement> & {
	// 	column: Column<TData, TValue>;
	// 	title: string;
	// };

	// let { column, class: className, title, ...restProps }: WithoutChildren<Props> = $props();
	let { column } = $props();
</script>

<!-- {#if !column?.getCanSort()}
	<div class={className} {...restProps}>
		{title}
	</div>
{:else} -->
<!-- <div class={cn("flex items-center", className)} {...restProps}> -->
<!-- <div class={cn("flex items-center", 'abc')} {...restProps}> -->
<div class={cn('flex items-center', 'abc')}>
	<!-- <DropdownMenu.Root>
			<DropdownMenu.Trigger>
				{#snippet child({ props })}
					<Button
						{...props}
						variant="ghost"
						size="sm"
						class="data-[state=open]:bg-accent -ml-3 h-8"
					>
						<span>
							{title}
						</span>
						{#if column.getIsSorted() === "desc"}
							<ArrowDown class="ml-2 size-4" />
						{:else if column.getIsSorted() === "asc"}
							<ArrowUp class="ml-2 size-4" />
						{:else}
							<CaretSort class="ml-2 size-4" />
						{/if}
					</Button>
				{/snippet}
			</DropdownMenu.Trigger>
			<DropdownMenu.Content align="start">
				<DropdownMenu.Item onclick={() => column.toggleSorting(false)}>
					<ArrowUp class="text-muted-foreground/70 mr-2 size-3.5" />
					Asc
				</DropdownMenu.Item>
				<DropdownMenu.Item onclick={() => column.toggleSorting(true)}>
					<ArrowDown class="text-muted-foreground/70 mr-2 size-3.5" />
					Desc
				</DropdownMenu.Item>
				<DropdownMenu.Separator />
			</DropdownMenu.Content>
		</DropdownMenu.Root> -->
</div>
<!-- {/if} -->
