<script lang="ts">
	import { BarChart, LineChart, Spline, Tooltip } from 'layerchart';

	import type { GroupedPlotEntry } from '$types';

	const catppMocha = ['#74c7ec', '#f5e0dc', '#cba6f7', '#94e2d5', '#f5c2e7', '#f9e2af'];
	// const edgyColors = ['#8839ef', '#179299', '#dc8a78', '#ea76cb', '#fe640b', '#209fb5'];
	const keyColors = catppMocha;

	import { curveCatmullRom } from 'd3-shape';

	let {
		barData = [] as GroupedPlotEntry[],
		lineData = [] as GroupedPlotEntry[],
		titleBarMetric,
		titleLineMetric
	} = $props();

	interface SeriesEntry {
		key: string;
		label: string;
		color: string;
	}

	function generateSeriesKeys(
		plotData: GroupedPlotEntry[],
		keyColors: string[],
		titleMetric: string
	): SeriesEntry[] {
		// Get unique keys excluding 'on_date'
		const uniqueKeys = Array.from(
			new Set(
				plotData.flatMap((plotRow) => Object.keys(plotRow).filter((key) => key !== 'on_date'))
			)
		);

		// Calculate total value for each key
		const keyTotals = uniqueKeys.map((key) => ({
			key,
			total: plotData.reduce((sum, row) => sum + (Number(row[key]) || 0), 0)
		}));

		// Sort by total value in ascending order instead of descending
		keyTotals.sort((a, b) => b.total - a.total);

		// Map to final format, using only as many keys as we have colors
		const seriesKeys = keyTotals.slice(0, keyColors.length).map((entry, index) => ({
			key: entry.key,
			label: entry.key ? entry.key.charAt(0).toUpperCase() + entry.key.slice(1) : titleMetric,
			color: keyColors[index]
		}));

		return seriesKeys;
	}

	let seriesKeysBar = $derived(generateSeriesKeys(barData, keyColors, titleBarMetric));
	let seriesKeysLine = $derived(generateSeriesKeys(lineData, keyColors, titleLineMetric));
</script>

<div class="h-[400px] grid [&>*]:col-start-1 [&>*]:row-start-1 p-4 border rounded">
	<BarChart
		data={barData}
		x="on_date"
		series={seriesKeysBar}
		seriesLayout="stack"
		grid={false}
		axis={false}
		padding={{ left: 16, bottom: 16 }}
		props={{
			yAxis: { format: 'metric' }
		}}
		legend={{ placement: 'top-right' }}
	></BarChart>

	<!-- Second chart (line), responsible for tooltip -->
	<BarChart
		data={lineData}
		x="on_date"
		series={seriesKeysLine}
		grid={false}
		yDomain={null}
		padding={{ left: 16, bottom: 16 }}
		props={{
			xAxis: { rule: true }
		}}
	>
		<svelte:fragment slot="marks">
			{#each seriesKeysLine as key}
				{console.log(key)}
				<Spline y={key.key} color={key.color} curve={curveCatmullRom} strokeWidth={3} />
			{/each}
		</svelte:fragment>

		<svelte:fragment slot="tooltip">
			<Tooltip.Root let:data>
				<Tooltip.Header>
					{data.on_date}
				</Tooltip.Header>
				<Tooltip.List>
					{#each seriesKeysLine as key}
						<Tooltip.Item label={key.label} value={`(line) ${data[key.key]}`} />
					{/each}
				</Tooltip.List>
			</Tooltip.Root>
		</svelte:fragment>
	</BarChart>
</div>
