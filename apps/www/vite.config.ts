import tailwindcss from '@tailwindcss/vite';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import { myDocsAssetPlugin } from './mkdocs-static-asset-plugin';

export default defineConfig({
	plugins: [tailwindcss(), sveltekit(), myDocsAssetPlugin()]
});
