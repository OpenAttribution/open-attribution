import { handler } from './build/handler.js';
import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';

const app = express();

// Get absolute path to assets folder using native Node.js modules
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const docsAssetsPath = path.join(__dirname, './static/generated-docs/assets');
const blogAssetsPath = path.join(__dirname, './static/generated-blog/assets');

app.use('/blog/assets', express.static(blogAssetsPath));
app.use('/docs/assets', express.static(docsAssetsPath));

// let SvelteKit handle everything else, including serving prerendered pages and static assets
app.use(handler);

app.listen(4173, () => {
	console.log('listening on port 0.0.0.0:4173');
});
