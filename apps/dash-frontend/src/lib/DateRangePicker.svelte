<script lang="ts">
	import { DateFormatter, getLocalTimeZone, today, type DateValue } from '@internationalized/date';
	import { RangeCalendar } from '$lib/components/ui/range-calendar/index.js';
	import type { MyDateRange } from '../types';
	type OnChangeCallback = (value: MyDateRange | undefined) => void;
	import * as Popover from '$lib/components/ui/popover/index.js';
	import CalendarIcon from 'lucide-svelte/icons/calendar';

	let defaultStartValue: DateValue = $state(today(getLocalTimeZone()).add({ days: -7 }));
	let defaultEndValue: DateValue = $state(today(getLocalTimeZone()));

	let { onChange }: { onChange: OnChangeCallback } = $props();

	let value: MyDateRange = $state({
		start: defaultStartValue,
		end: defaultEndValue
	});

	const df = new DateFormatter('en-CA', {
		dateStyle: 'medium'
	});

	$effect(() => {
		if (onChange) {
			onChange(value);
		}
	});
</script>

<div class="grid gap-2">
	<Popover.Root>
		<Popover.Trigger>
			<!-- <Button
				variant="outline"
				class={cn(
					'w-[300px] justify-start text-left font-normal',
					!value && 'text-muted-foreground'
				)}
			> -->
			<CalendarIcon class="mr-2 h-4 w-4" />
			{#if value && value.start}
				{#if value.end}
					{df.format(value.start.toDate(getLocalTimeZone()))} - {df.format(
						value.end.toDate(getLocalTimeZone())
					)}
				{:else}
					{df.format(value.start.toDate(getLocalTimeZone()))} - ???
				{/if}
			{:else if defaultStartValue}
				{df.format(defaultStartValue.toDate(getLocalTimeZone()))} -
				{df.format(defaultEndValue.toDate(getLocalTimeZone()))}
			{:else}
				Pick a date
			{/if}

			<!-- </Button> -->
		</Popover.Trigger>
		<Popover.Content class="w-auto p-0" align="start">
			<div class="grid gap-4">
				<RangeCalendar bind:value numberOfMonths={2} />
				<div></div>
			</div></Popover.Content
		>
	</Popover.Root>
</div>
