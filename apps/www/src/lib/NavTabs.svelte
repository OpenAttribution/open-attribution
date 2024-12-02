<script lang="ts">
	import { page } from '$app/stores';
	const topBarFont = 'text-base hover:text-primary-900-100';
	const topBarHighlightedFont = 'text-base text-primary-900-100';
	const horizontalDivider = 'h-12 w-px bg-surface-500';
	const topDivider = 'w-full border-t-[1px] md:border-t-0 md:border-b-[1px] border-surface-500 p-2';
	function isHighlighted(path: string) {
		if (path === '/') {
			if ($page.url.pathname === '/') {
				return true;
			} else {
				return false;
			}
		}

		return $page.url.pathname.startsWith(path);
	}
</script>

<div class="flex flex-row gap-2 md:gap-6 text-center items-center {topDivider} mx-2">
	<a href="/">
		<p class={isHighlighted('/') ? topBarHighlightedFont : topBarFont}>Home</p>
	</a>
	<div class={horizontalDivider}></div>

	<a href="/product" class={topBarFont}>
		<p class={isHighlighted('/product') ? topBarHighlightedFont : topBarFont}>Product</p>
	</a>

	<div class={horizontalDivider}></div>
	<a href="/docs" class={topBarFont}>
		<p class={isHighlighted('/docs') ? topBarHighlightedFont : topBarFont}>Documentation</p>
	</a>
	<div class={horizontalDivider}></div>
	<a href="/blog" class={topBarFont}>
		<p class={isHighlighted('/blog') ? topBarHighlightedFont : topBarFont}>Blog</p>
	</a>

	<div class={horizontalDivider}></div>
	<a href="/about" class={topBarFont}>
		<p class={isHighlighted('/about') ? topBarHighlightedFont : topBarFont}>About</p>
	</a>
</div>
