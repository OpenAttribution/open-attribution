import type { Actions, PageServerLoad } from './$types.js';
import { redirect } from '@sveltejs/kit';

export const actions = {
	integrations: async ({ request }) => {
		const data = await request.formData();
		const name = data.get('name');

		console.log(`hiiii ${name}`);
		console.log(`Network Name: ${name}`);

		const response = await fetch(`http://dash-backend:8001/api/networks/add/${name}`, {
			method: 'POST'
		});

		// Check if the request was successful
		if (!response.ok) {
			console.error('Failed to add the network');
			// Optionally, you could return some error state or message here
			return { error: 'Failed to add the network' };
		}

		// Redirect back to /integrations after successful form submission
		// throw redirect(303, '/integrations');
	}
} satisfies Actions;

export const load: PageServerLoad = async ({}) => {
	return {
		respData: fetch(`http://dash-backend:8001/api/networks`)
			.then((resp) => {
				if (resp.status === 200) {
					return resp.json();
				} else if (resp.status === 404) {
					console.log('Not found');
					return 'Not Found';
				} else if (resp.status === 500) {
					console.log('API Server error');
					return 'Backend Error';
				}
			})
			.then(
				(json) => json,
				(error) => {
					console.log('Uncaught error', error);
					return 'Uncaught Error';
				}
			)
	};
};
