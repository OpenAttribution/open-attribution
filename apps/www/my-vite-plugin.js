import express from 'express';

const assets = express.static('./static/documentation/assets');

const configureServer = (server) => {
	server.middlewares.use('/docs/assets', assets);
};

export const myVitePlugin = () => ({
	name: 'my-vite-plugin',
	configureServer,
	configurePreviewServer: configureServer
});
