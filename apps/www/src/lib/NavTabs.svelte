<script lang="ts">
	import { page } from '$app/stores';
	const topBarFont = 'text-base text-tertiary-800-200 hover:text-primary-800-200';
	const topBarHighlightedFont = 'text-base text-primary-800-200';
	const horizontalDivider = 'h-12 w-px md:hidden bg-surface-500';
	const mainClass = 'w-full p-1 md:p-2';
	const bottomDivider = 'md:hidden w-full border-b-[1px] border-surface-500 p-2';
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

<div class="flex flex-col">
	<div class={bottomDivider}></div>
	<div class="flex flex-row gap-2 md:gap-6 {mainClass} mx-2 place-content-center">
		<a href="/" class="hidden md:block">
			<p class={isHighlighted('/') ? topBarHighlightedFont : topBarFont}>Home</p>
		</a>
		<div class="hidden md:block {horizontalDivider}"></div>

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
</div>
