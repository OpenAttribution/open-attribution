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
	const appData = await fetch(`http://dash-backend:8001/api/apps/${storeid}`).then((res) =>
		res.json()
	);

	const appLinks = await fetch(`http://dash-backend:8001/api/apps/${appData.app.id}/links`).then(
		(res) => res.json()
	);

	console.log(`root layout load apps, networks end`);

	return {
		appData: appData,
		appLinks: appLinks
	};
};
