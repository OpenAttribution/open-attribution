import { purgeCss } from 'vite-plugin-tailwind-purgecss';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [
		sveltekit(),
		purgeCss()
		// I am unclear if this has ever helped worked, perhaps only after build?
		// {
		// 	name: 'docs-index',
		// 	configureServer(server) {
		// 		server.middlewares.use((req, res, next) => {
		// 			if (req.url?.startsWith('/docs')) {
		// 				req.url = req.url + '/index.html';
		// 			}
		// 			next();
		// 		});
		// 	}
		// }
	]
});
