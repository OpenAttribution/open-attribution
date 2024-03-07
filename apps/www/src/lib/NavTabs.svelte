<script lang="ts">
	import { page } from '$app/stores';
	import { TabGroup, TabAnchor } from '@skeletonlabs/skeleton';
</script>

<TabGroup
	active="variant-filled-primary"
	hover="hover:variant-soft-primary"
	flex="flex-1"
	rounded=""
	border=""
	class="w-full p-0"
>
	<TabAnchor class="p-0 px-0" href="/" selected={$page.url.pathname == '/'}>
		<h5 class="h6 md:h5 md:p-2">Home</h5>
	</TabAnchor>

	<TabAnchor class="p-0 px-0" href="/product" selected={$page.url.pathname.startsWith('/product')}>
		<h3 class="h6 md:h5 md:p-2">Product</h3>
	</TabAnchor>

	<TabAnchor class="p-0 px-0" href="/docs/" selected={$page.url.pathname.startsWith('/docs/')}>
		<h3 class="h6 md:h5 md:p-2">Documentation</h3>
	</TabAnchor>

	<TabAnchor class="p-0 px-0" href="/blog/" selected={$page.url.pathname.startsWith('/blog/')}>
		<h3 class="h6 md:h5 md:p-2">Blog</h3>
	</TabAnchor>

	<TabAnchor class="p-0 px-0" href="/about" selected={$page.url.pathname === '/about'}
		><h3 class="h6 md:h5 md:p-2">About</h3></TabAnchor
	>
</TabGroup>
