<script lang="ts">
	import { Chart, Svg, Axis, Bars, Highlight, Tooltip } from 'layerchart';

	import { scaleBand, scaleOrdinal } from 'd3-scale';

	import { sum } from 'd3-array';

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
					basket: 1,
					fruit: 'bananas',
					value: 1920
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
					basket: 1,
					fruit: 'bananas',
					value: 1440
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
					basket: 1,
					fruit: 'bananas',
					value: 1000
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
					basket: 1,
					fruit: 'bananas',
					value: 560
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
			fruit: 'bananas',
			keys: {
				year: 2019,
				fruit: 'bananas'
			},
			value: 1920,
			values: [3840, 5760],
			data: [
				{
					year: 2019,
					basket: 1,
					fruit: 'apples',
					value: 3840
				},
				{
					year: 2019,
					basket: 1,
					fruit: 'bananas',
					value: 1920
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
			fruit: 'bananas',
			keys: {
				year: 2018,
				fruit: 'bananas'
			},
			value: 1440,
			values: [1600, 3040],
			data: [
				{
					year: 2018,
					basket: 1,
					fruit: 'apples',
					value: 1600
				},
				{
					year: 2018,
					basket: 1,
					fruit: 'bananas',
					value: 1440
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
			fruit: 'bananas',
			keys: {
				year: 2017,
				fruit: 'bananas'
			},
			value: 1000,
			values: [820, 1820],
			data: [
				{
					year: 2017,
					basket: 1,
					fruit: 'apples',
					value: 820
				},
				{
					year: 2017,
					basket: 1,
					fruit: 'bananas',
					value: 1000
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
			fruit: 'bananas',
			keys: {
				year: 2016,
				fruit: 'bananas'
			},
			value: 560,
			values: [820, 1380],
			data: [
				{
					year: 2016,
					basket: 1,
					fruit: 'apples',
					value: 820
				},
				{
					year: 2016,
					basket: 1,
					fruit: 'bananas',
					value: 560
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
					basket: 1,
					fruit: 'bananas',
					value: 1920
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
					basket: 1,
					fruit: 'bananas',
					value: 1440
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
					basket: 1,
					fruit: 'bananas',
					value: 1000
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
					basket: 1,
					fruit: 'bananas',
					value: 560
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
					basket: 1,
					fruit: 'bananas',
					value: 1920
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
					basket: 1,
					fruit: 'bananas',
					value: 1440
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
					basket: 1,
					fruit: 'bananas',
					value: 1000
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
					basket: 1,
					fruit: 'bananas',
					value: 560
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
	const colorKeys = [...new Set(['cherries', 'grapes', 'bananas', 'apples'])];
	const keyColors = [
		'hsl(var(--color-info))',
		'hsl(var(--color-success))',
		'hsl(var(--color-warning))',
		'hsl(var(--color-danger))'
	];
</script>

<div class="h-[300px] p-4 border rounded">
	<Chart
		data={stackedData}
		x="year"
		xScale={scaleBand().paddingInner(0.4).paddingOuter(0.1)}
		y="values"
		yNice={4}
		c="fruit"
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
			<Highlight area />
		</Svg>

		<Tooltip.Root let:data>
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
				<Tooltip.Item
					label="total"
					value={sum([...data.data], (d) => d.value)}
					format="integer"
					valueAlign="right"
				/>
			</Tooltip.List>
		</Tooltip.Root>
	</Chart>
</div>
