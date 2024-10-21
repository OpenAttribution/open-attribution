<script lang="ts">
	import { Chart, Svg, Axis, Bars, Highlight, Tooltip } from 'layerchart';

	import { scaleBand, scaleOrdinal } from 'd3-scale';

	import { sum } from 'd3-array';

	import { schemeAccent, schemePastel1, schemeObservable10 } from 'd3-scale-chromatic';

	export let stackedData = [
		{
			year: 2019,
			fruit: 'apples',
			keys: {
				year: 2019,
				fruit: 'apples'
			},
			value: 3840,
			values: [0, 3840],
			data: [
				{
					year: 2019,
					basket: 1,
					fruit: 'apples',
					value: 3840
				},
				{
					year: 2019,
					basket: 2,
					fruit: 'cherries',
					value: 960
				},
				{
					year: 2019,
					basket: 2,
					fruit: 'grapes',
					value: 400
				}
			]
		},
		{
			year: 2018,
			fruit: 'apples',
			keys: {
				year: 2018,
				fruit: 'apples'
			},
			value: 1600,
			values: [0, 1600],
			data: [
				{
					year: 2018,
					basket: 1,
					fruit: 'apples',
					value: 1600
				},
				{
					year: 2018,
					basket: 2,
					fruit: 'cherries',
					value: 960
				},
				{
					year: 2018,
					basket: 2,
					fruit: 'grapes',
					value: 400
				}
			]
		},
		{
			year: 2017,
			fruit: 'apples',
			keys: {
				year: 2017,
				fruit: 'apples'
			},
			value: 820,
			values: [0, 820],
			data: [
				{
					year: 2017,
					basket: 1,
					fruit: 'apples',
					value: 820
				},
				{
					year: 2017,
					basket: 2,
					fruit: 'cherries',
					value: 640
				},
				{
					year: 2017,
					basket: 2,
					fruit: 'grapes',
					value: 400
				}
			]
		},
		{
			year: 2016,
			fruit: 'apples',
			keys: {
				year: 2016,
				fruit: 'apples'
			},
			value: 820,
			values: [0, 820],
			data: [
				{
					year: 2016,
					basket: 1,
					fruit: 'apples',
					value: 820
				},
				{
					year: 2016,
					basket: 2,
					fruit: 'cherries',
					value: 720
				},
				{
					year: 2016,
					basket: 2,
					fruit: 'grapes',
					value: 400
				}
			]
		},
		{
			year: 2019,
			fruit: 'cherries',
			keys: {
				year: 2019,
				fruit: 'cherries'
			},
			value: 960,
			values: [5760, 6720],
			data: [
				{
					year: 2019,
					basket: 1,
					fruit: 'apples',
					value: 3840
				},
				{
					year: 2019,
					basket: 2,
					fruit: 'cherries',
					value: 960
				},
				{
					year: 2019,
					basket: 2,
					fruit: 'grapes',
					value: 400
				}
			]
		},
		{
			year: 2018,
			fruit: 'cherries',
			keys: {
				year: 2018,
				fruit: 'cherries'
			},
			value: 960,
			values: [3040, 4000],
			data: [
				{
					year: 2018,
					basket: 1,
					fruit: 'apples',
					value: 1600
				},
				{
					year: 2018,
					basket: 2,
					fruit: 'cherries',
					value: 960
				},
				{
					year: 2018,
					basket: 2,
					fruit: 'grapes',
					value: 400
				}
			]
		},
		{
			year: 2017,
			fruit: 'cherries',
			keys: {
				year: 2017,
				fruit: 'cherries'
			},
			value: 640,
			values: [1820, 2460],
			data: [
				{
					year: 2017,
					basket: 1,
					fruit: 'apples',
					value: 820
				},
				{
					year: 2017,
					basket: 2,
					fruit: 'cherries',
					value: 640
				},
				{
					year: 2017,
					basket: 2,
					fruit: 'grapes',
					value: 400
				}
			]
		},
		{
			year: 2016,
			fruit: 'cherries',
			keys: {
				year: 2016,
				fruit: 'cherries'
			},
			value: 720,
			values: [1380, 2100],
			data: [
				{
					year: 2016,
					basket: 1,
					fruit: 'apples',
					value: 820
				},
				{
					year: 2016,
					basket: 2,
					fruit: 'cherries',
					value: 720
				},
				{
					year: 2016,
					basket: 2,
					fruit: 'grapes',
					value: 400
				}
			]
		},
		{
			year: 2019,
			fruit: 'grapes',
			keys: {
				year: 2019,
				fruit: 'grapes'
			},
			value: 400,
			values: [6720, 7120],
			data: [
				{
					year: 2019,
					basket: 1,
					fruit: 'apples',
					value: 3840
				},
				{
					year: 2019,
					basket: 2,
					fruit: 'cherries',
					value: 960
				},
				{
					year: 2019,
					basket: 2,
					fruit: 'grapes',
					value: 400
				}
			]
		},
		{
			year: 2018,
			fruit: 'grapes',
			keys: {
				year: 2018,
				fruit: 'grapes'
			},
			value: 400,
			values: [4000, 4400],
			data: [
				{
					year: 2018,
					basket: 1,
					fruit: 'apples',
					value: 1600
				},
				{
					year: 2018,
					basket: 2,
					fruit: 'cherries',
					value: 960
				},
				{
					year: 2018,
					basket: 2,
					fruit: 'grapes',
					value: 400
				}
			]
		},
		{
			year: 2017,
			fruit: 'grapes',
			keys: {
				year: 2017,
				fruit: 'grapes'
			},
			value: 400,
			values: [2460, 2860],
			data: [
				{
					year: 2017,
					basket: 1,
					fruit: 'apples',
					value: 820
				},
				{
					year: 2017,
					basket: 2,
					fruit: 'cherries',
					value: 640
				},
				{
					year: 2017,
					basket: 2,
					fruit: 'grapes',
					value: 400
				}
			]
		},
		{
			year: 2016,
			fruit: 'grapes',
			keys: {
				year: 2016,
				fruit: 'grapes'
			},
			value: 400,
			values: [2100, 2500],
			data: [
				{
					year: 2016,
					basket: 1,
					fruit: 'apples',
					value: 820
				},
				{
					year: 2016,
					basket: 2,
					fruit: 'cherries',
					value: 720
				},
				{
					year: 2016,
					basket: 2,
					fruit: 'grapes',
					value: 400
				}
			]
		}
	];

	export let wideData = [
		{
			year: 2019,
			apples: 3840,
			bananas: 1920,
			cherries: 960,
			grapes: 400
		},
		{
			year: 2018,
			apples: 1600,
			bananas: 1440,
			cherries: 960,
			grapes: 400
		},
		{
			year: 2017,
			apples: 820,
			bananas: 1000,
			cherries: 640,
			grapes: 400
		},
		{
			year: 2016,
			apples: 820,
			bananas: 560,
			cherries: 720,
			grapes: 400
		}
	];

	export let plotData = [
		{ year: '2021', group: 'apples', value: 29288 },
		{ year: '2022', group: 'apples', value: 26783 },
		{ year: '2023', group: 'apples', value: 22139 },
		{ year: '2024', group: 'apples', value: 21724 },
		{ year: '2021', group: 'cherries', value: 20852 },
		{ year: '2022', group: 'cherries', value: 18725 },
		{ year: '2023', group: 'grapes', value: 17417 },
		{ year: '2024', group: 'cherries', value: 15402 }
	];

	// const colorKeys = [...new Set(['cherries', 'grapes', 'bananas', 'apples'])];

	// Get the first 5 unique 'group' values
	$: colorKeys = Array.from(new Set(plotData.map((d) => d.group))).slice(0, 5);
	const keyColors = schemeObservable10;
</script>

<div class="h-[300px] p-4 border rounded">
	<Chart
		data={plotData}
		x="on_date"
		xScale={scaleBand().paddingInner(0.4).paddingOuter(0.1)}
		y="installs"
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
