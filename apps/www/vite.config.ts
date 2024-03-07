import { purgeCss } from 'vite-plugin-tailwind-purgecss';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

// Used for serving static mkbuild docs
import express from 'express';
const assets = express.static('./static/documentation/assets/');

export default defineConfig({
	plugins: [
		sveltekit(),
		purgeCss(),
		{
		name: 'docs-static-assets',
		configureServer(server) {
    		server.middlewares.use('/docs/assets', assets)
}
}
	]
});
