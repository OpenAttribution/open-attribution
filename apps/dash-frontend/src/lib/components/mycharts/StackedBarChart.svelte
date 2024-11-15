<script lang="ts">
	import { BarChart } from 'layerchart';

	import type { GroupedPlotEntry } from '../../../types';

	const catppMocha = ['#f5e0dc', '#cba6f7', '#94e2d5', '#f5c2e7', '#f9e2af', '#74c7ec'];
	// const edgyColors = ['#dc8a78','#8839ef','#179299','#ea76cb','#fe640b', '#209fb5'];
	const keyColors = catppMocha;

	let { plotData = [] as GroupedPlotEntry[] } = $props();

	interface SeriesEntry {
		key: string;
		label: string;
		color: string;
	}

	function generateSeriesKeys(plotData: GroupedPlotEntry[], keyColors: string[]): SeriesEntry[] {
		const uniqueKeys = Array.from(
			new Set(
				plotData.flatMap((plotRow) => Object.keys(plotRow).filter((key) => key !== 'on_date'))
			)
		);
		const seriesKeys = uniqueKeys.slice(0, keyColors.length).map((key, index) => ({
			key,
			label: key.charAt(0).toUpperCase() + key.slice(1),
			color: keyColors[index]
		}));

		return seriesKeys;
	}

	const seriesKeys = generateSeriesKeys(plotData, keyColors);
</script>

<div class="h-[300px] p-4 border rounded">
	<BarChart
		data={plotData}
		x="on_date"
		series={seriesKeys}
		seriesLayout="stack"
		props={{
			// xAxis: { format: 'date' },
			yAxis: { format: 'metric' }
		}}
		legend={{ placement: 'top-right', classes: { root: 'mt-2' } }}
	/>
</div>
