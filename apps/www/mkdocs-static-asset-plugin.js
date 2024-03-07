import express from 'express';

const docAssets = express.static('./static/generated-docs/assets');
const blogAssets = express.static('./static/generated-blog/assets');

const configureServer = (server) => {
server.middlewares.use('/docs/assets', docAssets);
server.middlewares.use('/blog/assets', blogAssets);
};

export const myDocsAssetPlugin = () => ({
	name: 'my-mkdocs-plugin',
	configureServer,
	configurePreviewServer: configureServer
});
