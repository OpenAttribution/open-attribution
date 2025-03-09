<script lang="ts">
	import StackedBar from '$lib/components/mycharts/StackedBarChart.svelte';
	import type { GroupedPlotEntry, DatesOverviewEntry, OverviewEntry } from '$types';

	import * as Card from '$lib/components/ui/card';
	import { Label } from '$lib/components/ui/label';
	import * as Select from '$lib/components/ui/select';

	import { page } from '$app/state';

	import {
		tableDimensions,
		baseMetricsLabels,
		specialMetricsLabels,
		retentionLables
	} from '$lib/constants';

	let { data, filteredNetworks, filteredApps } = $props();

	let groupByDimA = $state('');
	let titleGroupByA = $derived(lookupDimensionTitle(groupByDimA));

	const pageDefaultPlotBarMetric = 'installs';
	const pageDefaultPlotLineMetric = 'dau';

	let plotLineMetric = $state(pageDefaultPlotLineMetric);
	let plotBarMetric = $state(pageDefaultPlotBarMetric);

	function lookupDimensionTitle(dimension: string) {
		let myTitle = tableDimensions.find((dim) => dim.value === dimension)?.label || dimension;
		return myTitle;
	}

	let finalBarPlotData = $derived(
		getFinalPlotData(
			getFilteredPlotData(data.respData.dates_overview, filteredNetworks, filteredApps),
			groupByDimA,
			plotBarMetric
		)
	);

	let finalLinePlotData = $derived(
		getFinalPlotData(
			getFilteredPlotData(data.respData.dates_overview, filteredNetworks, filteredApps),
			groupByDimA,
			plotLineMetric
		)
	);

	function lookupMetricTitle(metric: string) {
		const allLabels = [...baseMetricsLabels, ...specialMetricsLabels, ...retentionLables];
		let myTitle = allLabels.find((m) => m.value === metric)?.label || metric;
		return myTitle;
	}

	let titleBarMetric = $derived(lookupMetricTitle(plotBarMetric));
	let titleLineMetric = $derived(lookupMetricTitle(plotLineMetric));

	function getFinalPlotData(
		myData: DatesOverviewEntry[],
		groupByKey: string = 'network',
		metric: string = 'installs'
	) {
		let myReturnedFinalPlotData: GroupedPlotEntry[] = [];
		if (myData && myData.length > 0) {
			myReturnedFinalPlotData = plotGroupByDimensions(myData, groupByKey, metric);
		} else {
			myReturnedFinalPlotData = [];
		}
		return myReturnedFinalPlotData;
	}

	function getFilteredPlotData(
		myData: DatesOverviewEntry[],
		myFilterNetworks: string[],
		myFilterApps: string[]
	) {
		let myFilteredData: DatesOverviewEntry[] = [];
		// console.log('PLOT FILTER START myData=', myData.length);
		if (myData && myData.length > 0) {
			myFilteredData = myData.filter((item) => {
				const networkMatch =
					myFilterNetworks.length === 0 || myFilterNetworks.includes(item.network);
				const appMatch = myFilterApps.length === 0 || myFilterApps.includes(item.store_id);
				return networkMatch && appMatch;
			});
		} else {
			myFilteredData = myData;
		}
		return myFilteredData;
	}

	function plotGroupByForBasicMetric(
		myFilteredData: OverviewEntry[],
		groupByKey: string,
		metric: string
	) {
		return myFilteredData.reduce<Record<string, Record<string, number>>>((acc, curr) => {
			const onDate = curr['on_date'] as string;

			let groupByValue = '';
			if (groupByKey == '') {
				groupByValue = metric;
			} else {
				groupByValue = curr[groupByKey] as string;
			}

			const metricValue = (curr[metric] as number) || 0;

			// Initialize the on_date if not present
			if (!acc[onDate]) {
				acc[onDate] = {};
			}

			// Add metric value for dimension
			acc[onDate][groupByValue] = (acc[onDate][groupByValue] || 0) + metricValue;

			return acc;
		}, {});
	}

	function plotGroupByForSpecialMetric(
		myFilteredData: OverviewEntry[],
		dimension: string,
		metric: string
	) {
		let numerator = '';
		let denominator = '';

		if (metric === 'ctr') {
			numerator = 'clicks';
			denominator = 'impressions';
		} else if (metric === 'ipm') {
			numerator = 'installs';
			denominator = 'impressions';
		}

		// First, group by date and dimension, summing any flat metrics
		const grouped = myFilteredData.reduce<{
			[date: string]: {
				[dimension: string]: {
					numeratorSum: number;
					denominatorSum: number;
				};
			};
		}>((acc, curr) => {
			const onDate = curr.on_date;
			const dimensionValue = curr[dimension] as string;
			const numeratorValue = (curr[numerator] as number) || 0;
			const denominatorValue = (curr[denominator] as number) || 0;

			// Initialize nested objects if they don't exist
			if (!acc[onDate]) {
				acc[onDate] = {};
			}
			if (!acc[onDate][dimensionValue]) {
				acc[onDate][dimensionValue] = {
					numeratorSum: 0,
					denominatorSum: 0
				};
			}

			// Sum up the values
			acc[onDate][dimensionValue].numeratorSum += numeratorValue;
			acc[onDate][dimensionValue].denominatorSum += denominatorValue;

			return acc;
		}, {});

		// Calculate final metrics by dividing sums
		const result: Record<string, Record<string, number>> = {};

		for (const date in grouped) {
			result[date] = {};
			for (const dim in grouped[date]) {
				const { numeratorSum, denominatorSum } = grouped[date][dim];
				if (metric === 'ctr') {
					result[date][dim] = denominatorSum > 0 ? numeratorSum / denominatorSum : 0;
				} else if (metric === 'ipm') {
					result[date][dim] = numeratorSum > 0 ? (numeratorSum / denominatorSum) * 1000 : 0;
				}
			}
		}

		return result;
	}

	function plotGroupByForRetentionMetric(
		myFilteredData: OverviewEntry[],
		dimension: string,
		metric: string
	) {
		// Remove 'ret_' prefix from metric name, so we can use it as a dimension
		const dx_metric = metric.replace('ret_', '');

		// First, group by date and dimension, summing any flat metrics
		const grouped = myFilteredData.reduce<{
			[date: string]: {
				[dimension: string]: {
					metricSum: number;
					installsSum: number;
				};
			};
		}>((acc, curr) => {
			const onDate = curr.on_date;
			const dimensionValue = curr[dimension] as string;
			const metricValue = (curr[dx_metric] as number) || 0;
			const installsValue = curr.installs || 0;

			// Initialize nested objects if they don't exist
			if (!acc[onDate]) {
				acc[onDate] = {};
			}
			if (!acc[onDate][dimensionValue]) {
				acc[onDate][dimensionValue] = {
					metricSum: 0,
					installsSum: 0
				};
			}

			// Sum up the values
			acc[onDate][dimensionValue].metricSum += metricValue;
			acc[onDate][dimensionValue].installsSum += installsValue;

			return acc;
		}, {});

		// Calculate final metrics by dividing sums
		const result: Record<string, Record<string, number>> = {};

		for (const date in grouped) {
			result[date] = {};
			for (const dim in grouped[date]) {
				const { metricSum, installsSum } = grouped[date][dim];
				result[date][dim] = installsSum > 0 ? metricSum / installsSum : 0;
			}
		}

		return result;
	}

	function plotGroupByDimensions(
		filteredData: DatesOverviewEntry[],
		groupByKey: string,
		metric: string
	): GroupedPlotEntry[] {
		const userStartDate = page.url.searchParams.get('start') || '';
		const userEndDate = page.url.searchParams.get('end') || '';

		let startDate = '';
		let endDate = '';

		if (userStartDate && userStartDate < filteredData[0]['on_date']) {
			startDate = userStartDate;
		} else {
			startDate = filteredData[0]['on_date'] as string;
		}

		if (userEndDate && userEndDate > filteredData[filteredData.length - 1]['on_date']) {
			endDate = userEndDate;
		} else {
			endDate = filteredData[filteredData.length - 1]['on_date'] as string;
		}

		// Generate array of all dates between start and end
		const dates: string[] = [];
		const currentDate = new Date(startDate);
		const lastDate = new Date(endDate);

		while (currentDate <= lastDate) {
			dates.push(currentDate.toISOString().split('T')[0]);
			currentDate.setDate(currentDate.getDate() + 1);
		}

		let groupedData: Record<string, Record<string, number>> = {};
		if (metric.startsWith('ret_')) {
			groupedData = plotGroupByForRetentionMetric(filteredData, groupByKey, metric);
		} else if (metric === 'ctr' || metric === 'ipm') {
			groupedData = plotGroupByForSpecialMetric(filteredData, groupByKey, metric);
		} else {
			groupedData = plotGroupByForBasicMetric(filteredData, groupByKey, metric);
		}

		const allDimensionValues = new Set<string>();
		Object.values(groupedData).forEach((dimensionValues) => {
			Object.keys(dimensionValues).forEach((dim) => allDimensionValues.add(dim));
		});

		// Create complete dataset with all dates
		const completeData = dates.reduce<Record<string, Record<string, number>>>((acc, date) => {
			acc[date] = acc[date] || {};
			// Initialize all dimension values to 0 for this date
			allDimensionValues.forEach((dim) => {
				if (dim != '') {
					acc[date][dim] = groupedData[date]?.[dim] || 0;
				}
			});
			return acc;
		}, {});

		const pivotedData = Object.entries(completeData).map(([on_date, dimensionValues]) => {
			return {
				on_date,
				...dimensionValues
			};
		});
		return pivotedData.sort((a, b) => a.on_date.localeCompare(b.on_date));
	}
</script>

<Card.Root class="xl:col-span-2">
	<Card.Header class="flex flex-row items-center">
		<div class="flex flex-row items-center gap-2">
			<div class="flex flex-col gap-2">
				<Label for="plotBarBy">Breakdown Dimension</Label>
				<Select.Root type="single" name="plotBarBy" bind:value={groupByDimA}>
					<Select.Trigger class="w-[180px]">
						{titleGroupByA}
					</Select.Trigger>
					<Select.Content>
						<Select.Group>
							<Select.GroupHeading>Group By</Select.GroupHeading>
							{#each tableDimensions as dimension}
								<Select.Item value={dimension.value} label={dimension.label}
									>{dimension.label}</Select.Item
								>
							{/each}
						</Select.Group>
					</Select.Content>
				</Select.Root>
			</div>
			<div class="flex flex-col gap-2">
				<Label for="plotBarMetric">Bar</Label>
				<Select.Root type="single" name="plotBarMetric" bind:value={plotBarMetric}>
					<Select.Trigger class="w-[180px]">
						{titleBarMetric}
					</Select.Trigger>
					<Select.Content>
						<Select.Group>
							<Select.GroupHeading>Bar</Select.GroupHeading>
							{#each baseMetricsLabels as metric}
								<Select.Item value={metric.value} label={metric.label}>{metric.label}</Select.Item>
							{/each}
						</Select.Group>
					</Select.Content>
				</Select.Root>
			</div>
			<div class="flex flex-col gap-2">
				<Label for="plotLineMetric">Line</Label>
				<Select.Root type="single" name="plotLineMetric" bind:value={plotLineMetric}>
					<Select.Trigger class="w-[180px]">
						{titleLineMetric}
					</Select.Trigger>
					<Select.Content>
						<Select.Group>
							<Select.GroupHeading>Metric</Select.GroupHeading>
							{#each [...baseMetricsLabels, ...specialMetricsLabels, ...retentionLables] as metric}
								<Select.Item value={metric.value} label={metric.label}>{metric.label}</Select.Item>
							{/each}
						</Select.Group>
					</Select.Content>
				</Select.Root>
			</div>
		</div>
	</Card.Header>

	<Card.Content>
		{#await data.respData}
			Loading...
		{:then plotData}
			{#if plotData.dates_overview && plotData.dates_overview.length > 0}
				<StackedBar
					barData={finalBarPlotData}
					lineData={finalLinePlotData}
					{titleBarMetric}
					{titleLineMetric}
					{groupByDimA}
				></StackedBar>
			{:else}
				Loading...
			{/if}
		{/await}
	</Card.Content>
</Card.Root>
