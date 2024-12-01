// import { purgeCss } from 'vite-plugin-tailwind-purgecss';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import { myDocsAssetPlugin } from './mkdocs-static-asset-plugin';

export default defineConfig({
	// plugins: [sveltekit(), purgeCss(), myDocsAssetPlugin()]
	plugins: [sveltekit(), myDocsAssetPlugin()]
});
