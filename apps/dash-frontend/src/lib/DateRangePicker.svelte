<script lang="ts">
	import CalendarIcon from 'lucide-svelte/icons/calendar';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import { DateFormatter, type DateValue, getLocalTimeZone, today } from '@internationalized/date';
	import { cn } from '$lib/utils.js';
	import { Button } from '$lib/components/ui/button/index.js';
	import { RangeCalendar } from '$lib/components/ui/range-calendar/index.js';
	import * as Popover from '$lib/components/ui/popover/index.js';

	import type { MyDateRange } from '../types';

	type OnChangeCallback = (value: MyDateRange | undefined) => void;
	let { onChange }: { onChange: OnChangeCallback } = $props();

	let value: MyDateRange | undefined = $state({
		start: today(getLocalTimeZone()).add({ days: -7 }),
		end: today(getLocalTimeZone())
	});

	const df = new DateFormatter('en-CA', {
		dateStyle: 'medium'
	});

	let startValue: DateValue | undefined = $state(today(getLocalTimeZone()).add({ days: -7 }));

	// let startValue = $state(value.start); // Track start value separately if needed

	$effect(() => {
		const queryStart = $page.url.searchParams.get('start');
		const queryEnd = $page.url.searchParams.get('end');

		// If both are missing, update the URL with default calendar values
		if (value) {
			if (!queryStart || !queryEnd) {
				const startDate = value.start.toString(); // Default start from the component
				const endDate = value.end.toString(); // Default end from the component

				// Update the URL with default date range
				goto(`?start=${startDate}&end=${endDate}`, { replaceState: true });
			}
		}
	});

	$effect(() => {
		if (onChange) {
			onChange(value);
		}
	});
</script>

<div class="grid gap-2">
	<Popover.Root openFocus>
		<Popover.Trigger asChild let:builder>
			<Button
				variant="outline"
				class={cn(
					'w-[300px] justify-start text-left font-normal',
					!value && 'text-muted-foreground'
				)}
				builders={[builder]}
			>
				<CalendarIcon class="mr-2 h-4 w-4" />
				{#if value && value.start}
					{#if value.end}
						{df.format(value.start.toDate(getLocalTimeZone()))} - {df.format(
							value.end.toDate(getLocalTimeZone())
						)}
					{:else}
						{df.format(value.start.toDate(getLocalTimeZone()))}
					{/if}
				{:else if startValue}
					{df.format(startValue.toDate(getLocalTimeZone()))}
				{:else}
					Pick a date
				{/if}
			</Button>
		</Popover.Trigger>
		<Popover.Content class="w-auto p-0" align="start">
			<RangeCalendar
				bind:value
				bind:startValue
				initialFocus
				numberOfMonths={2}
				placeholder={value?.start}
			/>
		</Popover.Content>
	</Popover.Root>
</div>
