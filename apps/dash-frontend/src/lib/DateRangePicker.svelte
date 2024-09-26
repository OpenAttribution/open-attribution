<script lang="ts">
	import CalendarIcon from 'lucide-svelte/icons/calendar';
	import type { DateRange } from 'bits-ui';
	import { DateFormatter, type DateValue, getLocalTimeZone, today } from '@internationalized/date';
	import { cn } from '$lib/utils.js';
	import { Button } from '$lib/components/ui/button/index.js';
	import { RangeCalendar } from '$lib/components/ui/range-calendar/index.js';
	import * as Popover from '$lib/components/ui/popover/index.js';
	// let { onChange, children, dateRange } = $props();
	type OnChangeCallback = (value: DateRange | undefined) => void;
	let { onChange, dateRange }: { onChange: OnChangeCallback; dateRange?: DateRange } = $props();

	// Local state
	let value: DateRange | undefined = $state({
		start: today(getLocalTimeZone()).add({ days: -7 }),
		end: today(getLocalTimeZone())
	});

	// let { value = $bindable() } = $props()

	const df = new DateFormatter('en-CA', {
		dateStyle: 'medium'
	});

	// Calculate the start date (7 days ago)
	const startDate = today(getLocalTimeZone()).add({ days: -7 });

	// // Set the value to the range from today to the past 7 days
	// export let value: DateRange | undefined = {
	// 	start: startDate,
	// 	end: today(getLocalTimeZone())
	// };

	// let startValue: DateValue | undefined = undefined;

	let startValue: DateValue | undefined = $state(undefined);

	// Effect to watch for changes in `value` and call onChange prop
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
