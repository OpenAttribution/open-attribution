import { handler } from './build/handler.js';
import express from 'express';

const app = express();

// Get absolute path to assets folder, "./data/assets" might work fine and you can remove this line/dep
//const assetsPath = desm.join(import.meta.url, './static/generated-docs/assets');

// Serve your "data/assets" folder
app.use(express.static('/home/james/open-attribution/apps/www/static/generated-docs/assets/'));
app.use(
	'/blog/assets',
	express.static('/home/james/open-attribution/apps/www/static/generated-blog/assets/')
);

// let SvelteKit handle everything else, including serving prerendered pages and static assets
app.use(handler);

app.listen(3000, () => {
	console.log('listening on port 3000');
});
