import { purgeCss } from 'vite-plugin-tailwind-purgecss';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import { myVitePlugin } from './my-vite-plugin';

// export default defineConfig({
export default defineConfig(({ command, mode, ssrBuild }) => {
	return {
		plugins: [
			sveltekit(),
			purgeCss(),
			myVitePlugin()
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
			// 		{
			// 		name: 'docs-static-assets',
			// 		configureServer(server) {
			//     		server.middlewares.use('/docs/assets', assets)
			// }
			// },
			// { name: 'testtest',
			// 		configureServer(server) {
			// 			server.middlewares.use((req, res, next) => {
			// 					if (req.url?.startsWith('/docs')) {
			// 						req.url = req.url + '/index.html';
			// 					}
			// 					next();
			// 				});
			// 			}
			// 		}
		]
		// );
		// }
	};
});
