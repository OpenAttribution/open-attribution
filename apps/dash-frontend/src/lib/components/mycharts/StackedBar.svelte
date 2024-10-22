<script lang="ts">
	import { Chart, Svg, Axis, Bars, Highlight, Tooltip } from 'layerchart';

	import { scaleBand, scaleOrdinal } from 'd3-scale';

	import { sum } from 'd3-array';

	import { type GroupedEntry } from '../../../types';

	import { schemeAccent, schemePastel1, schemeObservable10 } from 'd3-scale-chromatic';

	// export let wideData = [
	// 	{
	// 		year: 2019,
	// 		apples: 3840,
	// 		bananas: 1920,
	// 		cherries: 960,
	// 		grapes: 400
	// 	},
	// 	{
	// 		year: 2018,
	// 		apples: 1600,
	// 		bananas: 1440,
	// 		cherries: 960,
	// 		grapes: 400
	// 	},
	// 	{
	// 		year: 2017,
	// 		apples: 820,
	// 		bananas: 1000,
	// 		cherries: 640,
	// 		grapes: 400
	// 	},
	// 	{
	// 		year: 2016,
	// 		apples: 820,
	// 		bananas: 560,
	// 		cherries: 720,
	// 		grapes: 400
	// 	}
	// ];

	let { plotData = [] as GroupedEntry[], plotGroup = 'network' } = $props();

	// const colorKeys = [...new Set(['cherries', 'grapes', 'bananas', 'apples'])];

	let colorKeys = $state<string[]>(['google', 'ironsource']);

	// Get the first 5 unique 'group' values

	// $effect(() => {
	// 	if (plotData) {
	// 		colorKeys = Array.from(new Set(plotData.map((d) => d.network))).slice(0, 5);
	// 	}
	console.log('PLOT DATA KEYS: AFTER IF ', colorKeys);
	// });

	console.log('PLOT DATA ROWS: AFTER IF ', plotData);
	const keyColors = schemeObservable10;

	// const plotData = [{'on_date': '2024-10-17', 'network': 'google', 'impressions': 1018.0}, {'on_date': '2024-10-17', 'network': 'google', 'impressions': 1018.0}, {'on_date': '2024-10-17', 'network': 'ironsource', 'impressions': 1048.0}, {'on_date': '2024-10-17', 'network': 'ironsource', 'impressions': 1048.0}, {'on_date': '2024-10-17', 'network': 'meta', 'impressions': 1026.0}]
</script>

<div class="h-[300px] p-4 border rounded">
	<Chart
		data={plotData}
		x="on_date"
		xScale={scaleBand().paddingInner(0.4).paddingOuter(0.1)}
		y="impressions"
		yNice={4}
		c="network"
		cScale={scaleOrdinal()}
		cDomain={colorKeys}
		cRange={keyColors}
		padding={{ left: 16, bottom: 24 }}
		tooltip={{ mode: 'band' }}
		let:cScale
	>
		<Svg>
			<Axis placement="left" grid rule />
			<Axis placement="bottom" rule />
			<Bars radius={4} strokeWidth={1} />
			<!-- <Highlight area /> -->
		</Svg>

		<!-- <Tooltip.Root let:data>
			<Tooltip.Header>{data.year}</Tooltip.Header>
			<Tooltip.List>
				{#each data.data as d}
					<Tooltip.Item
						label={d.fruit}
						value={d.value}
						color={cScale?.(d.fruit)}
						format="integer"
						valueAlign="right"
					/>
				{/each}

				<Tooltip.Separator />

				<!-- TODO: Remove [...] type hack to make svelte-check happy -->
		<!-- <Tooltip.Item
					label="total"
					value={sum([...data.data], (d) => d.value)}
					format="integer"
					valueAlign="right"
				/> -->
		<!-- </Tooltip.List> -->
		<!-- </Tooltip.Root> --> -->
	</Chart>
</div>
