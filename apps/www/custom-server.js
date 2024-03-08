import { handler } from './build/handler.js';
import express from 'express';
import { join } from 'desm';

const app = express();

// Get absolute path to assets folder
const docsAssetsPath = join(import.meta.url, './static/generated-docs/assets');
const blogAssetsPath = join(import.meta.url, './static/generated-blog/assets');

app.use('/docs/assets', express.static(docsAssetsPath));
app.use('/blog/assets', express.static(blogAssetsPath));

// let SvelteKit handle everything else, including serving prerendered pages and static assets
app.use(handler);

app.listen(4173, () => {
	console.log('listening on port 0.0.0.0:4173');
});
