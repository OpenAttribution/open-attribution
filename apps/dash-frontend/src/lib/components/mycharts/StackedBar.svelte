<script lang="ts">
	import { Chart, Svg, Axis, Bars, Tooltip } from 'layerchart';

	import { scaleBand, scaleOrdinal } from 'd3-scale';
	import { sum } from 'd3-array';


	import { type GroupedEntry } from '../../../types';

	import { schemeObservable10 } from 'd3-scale-chromatic';

	let { plotData = [] as GroupedEntry[], plotGroup = 'network' } = $props();

	let colorKeys = $state<string[]>(['google', 'ironsource']);


		if (plotData) {
			// Get the first 5 unique 'group' values
			colorKeys = Array.from(new Set(plotData.map((d) => d.network))).slice(0, 5);
		}

	console.log('PLOT DATA KEYS: AFTER IF ', colorKeys);

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

		<Tooltip.Root let:data>
			<Tooltip.Header>{data.on_date}</Tooltip.Header>
			<Tooltip.List>
				<!-- {#each data as d} -->
					<Tooltip.Item
						label={data.network}
						value={data.impressions}
						color={cScale?.(d.network)}
						format="integer"
						valueAlign="right"
					/>
				<!-- {/each} -->

				<Tooltip.Separator />

				<!-- TODO: Remove [...] type hack to make svelte-check happy -->
				<!-- <Tooltip.Item
					label="total"
					value={sum([...plotData], (d) => d.impressions)}
					format="integer"
					valueAlign="right"
				/> -->
		</Tooltip.List>
		</Tooltip.Root>
	</Chart>
</div>
