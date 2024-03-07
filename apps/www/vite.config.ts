import { purgeCss } from 'vite-plugin-tailwind-purgecss';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import { myDocsAssetPlugin } from './mkdocs-static-asset-plugin';


export default defineConfig({
// export default defineConfig(({ command, mode, ssrBuild }) => {
	// return {
		plugins: [
			sveltekit(),
			purgeCss(),
			myDocsAssetPlugin(),
			
		]
	}
);
