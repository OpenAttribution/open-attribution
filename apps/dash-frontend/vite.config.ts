import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [sveltekit()],
	server: {
		port: 4173, // Set your desired port here
		host: '0.0.0.0',
		strictPort: true // Prevent fallback to another port if this one is taken
	}
});
