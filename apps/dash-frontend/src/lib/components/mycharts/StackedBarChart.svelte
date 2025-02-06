<script lang="ts">
	import { BarChart, Spline } from 'layerchart';

	import type { GroupedPlotEntry } from '$types';

	const catppMocha = ['#74c7ec', '#f5e0dc', '#cba6f7', '#94e2d5', '#f5c2e7', '#f9e2af'];
	// const edgyColors = ['#dc8a78','#8839ef','#179299','#ea76cb','#fe640b', '#209fb5'];
	const keyColors = catppMocha;

	let { plotData = [] as GroupedPlotEntry[], lineData = [] as GroupedPlotEntry[] } = $props();

	interface SeriesEntry {
		key: string;
		label: string;
		color: string;
	}

	function generateSeriesKeys(plotData: GroupedPlotEntry[], keyColors: string[]): SeriesEntry[] {
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
			label: entry.key.charAt(0).toUpperCase() + entry.key.slice(1),
			color: keyColors[index]
		}));

		return seriesKeys;
	}

	let seriesKeys = $derived(generateSeriesKeys(plotData, keyColors));
</script>

<div class="h-[400px] grid [&>*]:col-start-1 [&>*]:row-start-1 p-4 border rounded">
	<BarChart
		data={plotData}
		x="on_date"
		series={seriesKeys}
		seriesLayout="stack"
		grid={false}
		axis={false}
		padding={{ left: 16, bottom: 16 }}
		props={{
			yAxis: { format: 'metric' }
		}}
		legend={{ placement: 'top-right' }}
	/>

	<!-- Second chart (line), responsible for tooltip -->
	<BarChart
		data={lineData}
		x="on_date"
		series={seriesKeys}
		yDomain={null}
		padding={{ left: 16, bottom: 16 }}
		props={{
			xAxis: { rule: true }
		}}
	>
		<svelte:fragment slot="marks">
			{#each seriesKeys as key}
				<Spline y={key.key} color={key.color} />
			{/each}
		</svelte:fragment>
	</BarChart>
</div>
