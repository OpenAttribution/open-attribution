import type { Actions, PageServerLoad } from './$types.js';

export const actions = {
	deleteApp: async ({ request }) => {
		const data = await request.formData();
		const id = data.get('id');

		console.log(`Delete app id: ${id}`);

		const response = await fetch(`http://dash-backend:8001/api/networks/${id}`, {
			method: 'DELETE'
		});

		// Check if the request was successful
		if (!response.ok) {
			console.error('Failed to delete the app');
			return { error: 'Failed to delete the app' };
		}
	}
} satisfies Actions;

export const load: PageServerLoad = async ({ params }) => {
	const storeid = params.storeid;

	return {
		appData: fetch(`http://dash-backend:8001/api/apps/${storeid}`)
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
