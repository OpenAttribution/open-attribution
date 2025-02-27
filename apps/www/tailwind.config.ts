import type { Config } from 'tailwindcss';

export default {
	darkMode: 'selector',

	content: ['./src/**/*.{html,js,svelte,ts}'],

	theme: {
		extend: {}
	},

	plugins: []
} satisfies Config;
